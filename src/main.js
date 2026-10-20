import { Actor, log } from 'apify';

import { finalize, SOURCES } from './normalize.js';
import { COLLECTORS } from './sources.js';

const STATE_STORE = 'customer-insights-state';
const SEEN_IDS_KEY = 'SEEN_IDS';
const MAX_SEEN_IDS = 50_000;
const PAGE_SIZE = 1000;

await Actor.init();

const input = {
    sources: SOURCES,
    lookbackDays: 8,
    threadMaxAgeDays: 30,
    dropEmojiOnly: true,
    deleteRawData: true,
    skipAlreadyDelivered: true,
    historyDatasetName: 'customer-insights',
    maxCostPerSourceUsd: 2,
    appStoreAppId: '1163368801',
    appStoreCountry: 'cz',
    appStoreMaxReviews: 500,
    googlePlayAppId: 'cz.csas.georgego',
    googlePlayMaxReviews: 2000,
    redditQueries: ['"česká spořitelna"', '"ceska sporitelna"', 'spořitelna george'],
    redditCzechSubreddits: ['czech', 'Prague', 'czechfinance', 'Brno', 'Czechia', 'czechrepublic'],
    redditMaxPostsPerQuery: 50,
    redditMaxCommentsPerPost: 500,
    facebookPageUrl: 'https://www.facebook.com/ceskasporitelna/',
    instagramProfileUrl: 'https://www.instagram.com/ceskasporitelna/',
    linkedinCompanyUrl: 'https://www.linkedin.com/company/10700/',
    maxPostsPerPage: 50,
    maxCommentsPerPost: 500,
    ...(await Actor.getInput()),
};

const client = Actor.apifyClient;
const until = new Date();
const since = new Date(until.getTime() - input.lookbackDays * 24 * 60 * 60 * 1000);
log.info(`Collecting feedback from ${since.toISOString()} to ${until.toISOString()}`, { sources: input.sources });

// Raw datasets hold author names and profile links, so we remember them and
// delete them once the cleaned records are saved.
const rawDatasetIds = [];

async function runActor(actorId, actorInput) {
    log.info(`Starting ${actorId}`);
    const run = await client.actor(actorId).call(actorInput, {
        maxTotalChargeUsd: input.maxCostPerSourceUsd,
        log: null,
    });
    rawDatasetIds.push(run.defaultDatasetId);
    if (run.status !== 'SUCCEEDED') {
        throw new Error(`${actorId} finished with status ${run.status} (run ${run.id})`);
    }
    const items = [];
    for (let offset = 0; ; offset += PAGE_SIZE) {
        const page = await client.dataset(run.defaultDatasetId).listItems({ offset, limit: PAGE_SIZE, clean: true });
        items.push(...page.items);
        if (page.items.length < PAGE_SIZE) break;
    }
    log.info(`${actorId} returned ${items.length} rows (run ${run.id})`);
    return items;
}

const context = { input, since, lookbackDays: input.lookbackDays, runActor };
const settled = await Promise.allSettled(input.sources.map((source) => COLLECTORS[source](context)));

const summary = { since: since.toISOString(), until: until.toISOString(), sources: {} };
const collected = [];
settled.forEach((result, i) => {
    const source = input.sources[i];
    if (result.status === 'fulfilled') {
        collected.push(...result.value);
        summary.sources[source] = { status: 'ok', rawRecords: result.value.length };
    } else {
        log.exception(result.reason, `Source ${source} failed`);
        summary.sources[source] = { status: 'failed', error: String(result.reason?.message || result.reason) };
    }
});

const { records, stats } = finalize(collected, { since, until, dropEmojiOnly: input.dropEmojiOnly });

// Overlapping windows (lookbackDays > 7 for a weekly schedule) would deliver
// the same item twice, so skip anything an earlier run already delivered.
const state = await Actor.openKeyValueStore(STATE_STORE);
const seen = new Set((await state.getValue(SEEN_IDS_KEY)) || []);
const fresh = input.skipAlreadyDelivered ? records.filter((r) => !seen.has(r.id)) : records;
stats.alreadyDelivered = records.length - fresh.length;

await Actor.pushData(fresh);
if (input.historyDatasetName) {
    const history = await Actor.openDataset(input.historyDatasetName);
    await history.pushData(fresh);
}

const updatedSeen = [...seen, ...fresh.map((r) => r.id)].slice(-MAX_SEEN_IDS);
await state.setValue(SEEN_IDS_KEY, updatedSeen);

for (const source of input.sources) {
    if (summary.sources[source].status === 'ok') {
        summary.sources[source].delivered = fresh.filter((r) => r.source === source).length;
    }
}
summary.delivered = fresh.length;
summary.dropped = stats;
await Actor.setValue('SUMMARY', summary);
log.info('Summary', summary);

if (input.deleteRawData) {
    for (const id of rawDatasetIds) {
        await client.dataset(id).delete().catch((err) => log.warning(`Could not delete raw dataset ${id}: ${err.message}`));
    }
}

const failed = input.sources.filter((s) => summary.sources[s].status === 'failed');
if (failed.length === input.sources.length) {
    await Actor.fail(`All sources failed: ${failed.join(', ')}`);
} else {
    const note = failed.length ? ` Failed sources: ${failed.join(', ')}.` : '';
    await Actor.exit(`Delivered ${fresh.length} new items.${note}`);
}
