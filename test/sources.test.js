// Runs every collector against canned scraper rows (shaped like real output,
// with fake people) to check the inputs we send and that no author data leaks.

import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ACTORS, COLLECTORS } from '../src/sources.js';

const input = {
    threadMaxAgeDays: 30,
    appStoreAppId: '1163368801',
    appStoreCountry: 'cz',
    appStoreMaxReviews: 500,
    googlePlayAppId: 'cz.csas.georgego',
    googlePlayMaxReviews: 2000,
    redditQueries: ['"česká spořitelna"'],
    redditCzechSubreddits: ['czech'],
    redditMaxPostsPerQuery: 50,
    redditMaxCommentsPerPost: 500,
    facebookPageUrl: 'https://www.facebook.com/ceskasporitelna/',
    instagramProfileUrl: 'https://www.instagram.com/ceskasporitelna/',
    linkedinCompanyUrl: 'https://www.linkedin.com/company/10700/',
    maxPostsPerPage: 50,
    maxCommentsPerPost: 500,
};
const since = new Date('2026-10-12T00:00:00Z');

const RESPONSES = {
    [ACTORS.facebookPosts]: [
        { url: 'https://www.facebook.com/ceskasporitelna/posts/p1', comments: 2, text: 'Tak je utrácejte' },
        { url: 'https://www.facebook.com/ceskasporitelna/posts/p2', comments: 0, text: 'Bez komentářů' },
    ],
    [ACTORS.facebookComments]: [
        { id: 'c1', commentId: '111', date: '2026-10-19T15:22:41.000Z', text: 'Reklamace katastrofa', profileName: 'Jana Nováková', profileUrl: 'https://fb/jana', commentUrl: 'https://fb/p1?comment_id=111', postTitle: 'Tak je utrácejte' },
        { id: 'c2', commentId: '112', date: '2026-10-19T16:00:00.000Z', text: 'Dobrý den, napište nám', profileName: 'Česká spořitelna', commentUrl: 'https://fb/p1?comment_id=112', postTitle: 'Tak je utrácejte' },
    ],
    [ACTORS.instagramPosts]: [
        { url: 'https://www.instagram.com/p/DellsqJilj1/', commentsCount: 6, caption: 'Tak je utrácejte 💙' },
        { url: 'https://www.instagram.com/p/DetQndHHNgk/', commentsCount: 0, caption: 'Život je lajf' },
    ],
    [ACTORS.instagramComments]: [
        { id: '183', postUrl: 'https://www.instagram.com/p/DellsqJilj1/', commentUrl: 'https://www.instagram.com/p/DellsqJilj1/c/183', text: 'Přesně tak', ownerUsername: 'petr.k', timestamp: '2026-10-17T12:39:14.000Z' },
        { id: '184', postUrl: 'https://www.instagram.com/p/DellsqJilj1/', commentUrl: 'https://www.instagram.com/p/DellsqJilj1/c/184', text: 'Děkujeme!', ownerUsername: 'ceskasporitelna', timestamp: '2026-10-17T13:00:00.000Z' },
    ],
    [ACTORS.linkedin]: [
        { type: 'post', id: '7516777126432403456', content: 'Lunch & Learn o AI', linkedinUrl: 'https://li/post' },
        { type: 'comment', id: '7516825237791997953', postId: '7516777126432403456', createdAt: '2026-10-16T11:39:52.550Z', commentary: 'Za 17 měsíců se toho posunulo', linkedinUrl: 'https://li/c', actor: { type: 'profile', author: false, name: 'Karel Dvořák', position: 'Analyst', linkedinUrl: 'https://li/in/karel' } },
        { type: 'comment', id: '7516825237791997954', postId: '7516777126432403456', createdAt: '2026-10-16T12:00:00.000Z', commentary: 'Děkujeme!', linkedinUrl: 'https://li/c2', actor: { type: 'company', author: true, name: 'Česká spořitelna' } },
    ],
    [ACTORS.appStore]: [{ id: '1', date: '2026-10-18T00:00:00.000Z', score: 5, title: 'Super', text: 'Super', userName: 'x' }],
    [ACTORS.googlePlay]: [{ reviewId: 'r1', rating: 2, timestamp: 1792061165, date: '2026-10-15', body: 'Složité', reviewer: 'Eva' }],
    [ACTORS.reddit]: [
        { _type: 'post', id: '1wwn4bc', subreddit: 'czech', title: 'Dotaz', selftext: 'George', createdAt: '2026-10-13T13:20:41.000000+0000', permalink: '/r/czech/comments/1wwn4bc/dotaz/', author: 'redditor1' },
    ],
};

function fakeRunner() {
    const calls = [];
    const runActor = async (actorId, actorInput) => {
        calls.push({ actorId, actorInput });
        return RESPONSES[actorId] ?? [];
    };
    return { calls, runActor };
}

const PERSONAL = ['Jana', 'Nováková', 'petr.k', 'Karel', 'Dvořák', 'redditor1', 'Eva', 'https://fb/jana'];

for (const [source, collect] of Object.entries(COLLECTORS)) {
    test(`${source}: records carry no author data`, async () => {
        const { runActor } = fakeRunner();
        const records = await collect({ input, since, lookbackDays: 8, runActor });
        assert.ok(records.length > 0);
        const json = JSON.stringify(records);
        for (const word of PERSONAL) assert.ok(!json.includes(word), `${source} leaked "${word}"`);
        for (const r of records) assert.equal(r.source, source);
    });
}

test('facebook: only posts with comments are scraped and the bank\'s replies are dropped', async () => {
    const { calls, runActor } = fakeRunner();
    const records = await COLLECTORS.facebook({ input, since, lookbackDays: 8, runActor });
    const commentsCall = calls.find((c) => c.actorId === ACTORS.facebookComments);
    assert.deepEqual(commentsCall.actorInput.startUrls, [{ url: 'https://www.facebook.com/ceskasporitelna/posts/p1' }]);
    assert.equal(commentsCall.actorInput.onlyCommentsNewerThan, '2026-10-12');
    assert.deepEqual(records.map((r) => r.text), ['Reklamace katastrofa']);
    assert.equal(records[0].context, 'Tak je utrácejte');
});

test('instagram: comments get the post caption as context, bank replies dropped', async () => {
    const { runActor } = fakeRunner();
    const records = await COLLECTORS.instagram({ input, since, lookbackDays: 8, runActor });
    assert.deepEqual(records.map((r) => [r.text, r.context]), [['Přesně tak', 'Tak je utrácejte 💙']]);
});

test('linkedin: comments get the post text as context', async () => {
    const { calls, runActor } = fakeRunner();
    const records = await COLLECTORS.linkedin({ input, since, lookbackDays: 8, runActor });
    assert.equal(records.length, 1);
    assert.equal(records[0].context, 'Lunch & Learn o AI');
    assert.equal(calls[0].actorInput.postedLimit, 'month');
    assert.equal(calls[0].actorInput.commentsPostedLimit, 'month');
});

test('google_play: seconds timestamp becomes the right date', async () => {
    const { runActor } = fakeRunner();
    const [record] = await COLLECTORS.google_play({ input, since, lookbackDays: 8, runActor });
    assert.equal(record.date, '2026-10-15T10:46:05.000Z');
});
