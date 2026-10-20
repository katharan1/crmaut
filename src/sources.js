// One collector per source. Each collector runs the Store Actor(s) it needs
// through `runActor`, and maps the raw rows to Customer Insights records.
//
// Comments arrive on old posts too, so for social sources we look at posts from
// the last `threadMaxAgeDays` days and keep only the comments made inside the
// run's date window.

import {
    mapAppStore, mapFacebook, mapGooglePlay, mapInstagram, mapLinkedIn, mapReddit,
    normalizeInstagramUrl, redditPostId, relevantRedditThreads,
} from './normalize.js';

export const ACTORS = {
    appStore: 'thewolves/appstore-reviews-scraper',
    googlePlay: 'neatrat/google-play-store-reviews-scraper',
    reddit: 'clearpath/reddit-post-comments-bulk-scraper',
    facebookPosts: 'apify/facebook-posts-scraper',
    facebookComments: 'apify/facebook-comments-scraper',
    instagramPosts: 'apify/instagram-scraper',
    instagramComments: 'apify/instagram-comment-scraper',
    linkedin: 'harvestapi/linkedin-company-posts',
};

// The bank's own replies under its posts are not customer feedback.
const OWN_ACCOUNT = /česká spořitelna|ceska sporitelna|^ceskasporitelna$/i;

function linkedinPeriod(days) {
    if (days <= 1) return '24h';
    if (days <= 7) return 'week';
    if (days <= 31) return 'month';
    if (days <= 93) return '3months';
    if (days <= 186) return '6months';
    if (days <= 365) return 'year';
    return 'any';
}

export async function collectAppStore({ input, runActor }) {
    const { appStoreAppId: appId, appStoreCountry: country, appStoreMaxReviews } = input;
    const items = await runActor(ACTORS.appStore, {
        appIds: [appId],
        country,
        maxItems: appStoreMaxReviews,
    });
    return items.map((item) => mapAppStore(item, { appId, country }));
}

export async function collectGooglePlay({ input, lookbackDays, runActor }) {
    const appId = input.googlePlayAppId;
    const items = await runActor(ACTORS.googlePlay, {
        appIdOrUrl: appId,
        sortBy: 'newest',
        recentDays: lookbackDays,
        maxReviews: input.googlePlayMaxReviews,
        pagesToScrape: -1,
        reviewsPerPage: 100,
        uniqueOnly: true,
    });
    return items.map((item) => mapGooglePlay(item, { appId }));
}

export async function collectReddit({ input, lookbackDays, runActor }) {
    const items = await runActor(ACTORS.reddit, {
        queries: input.redditQueries,
        searchSort: 'new',
        maxPostsPerQuery: input.redditMaxPostsPerQuery,
        maxPostAgeHours: input.threadMaxAgeDays * 24,
        maxCommentAgeHours: lookbackDays * 24,
        maxCommentsPerPost: input.redditMaxCommentsPerPost,
        expandAllComments: true,
        sort: 'new',
    });
    const relevant = relevantRedditThreads(items, input.redditCzechSubreddits);
    return items
        .filter((item) => relevant.has(redditPostId(item)))
        .map(mapReddit);
}

export async function collectFacebook({ input, since, runActor }) {
    const posts = await runActor(ACTORS.facebookPosts, {
        startUrls: [{ url: input.facebookPageUrl }],
        onlyPostsNewerThan: `${input.threadMaxAgeDays} days`,
        resultsLimit: input.maxPostsPerPage,
    });
    const urls = posts.filter((p) => p.url && (p.comments ?? 1) > 0).map((p) => ({ url: p.url }));
    if (urls.length === 0) return [];
    const comments = await runActor(ACTORS.facebookComments, {
        startUrls: urls,
        resultsLimit: input.maxCommentsPerPost * urls.length,
        includeNestedComments: true,
        viewOption: 'RECENT_ACTIVITY',
        onlyCommentsNewerThan: since.toISOString().slice(0, 10),
    });
    return comments
        .filter((c) => !OWN_ACCOUNT.test(c.profileName || c.author?.name || ''))
        .map(mapFacebook);
}

export async function collectInstagram({ input, runActor }) {
    const posts = await runActor(ACTORS.instagramPosts, {
        directUrls: [input.instagramProfileUrl],
        resultsType: 'posts',
        onlyPostsNewerThan: `${input.threadMaxAgeDays} days`,
        resultsLimit: input.maxPostsPerPage,
    });
    const withComments = posts.filter((p) => p.url && p.commentsCount > 0);
    if (withComments.length === 0) return [];
    const captions = new Map(withComments.map((p) => [normalizeInstagramUrl(p.url), p.caption]));
    const comments = await runActor(ACTORS.instagramComments, {
        directUrls: withComments.map((p) => p.url),
        resultsLimit: input.maxCommentsPerPost,
    });
    return comments
        .filter((c) => !OWN_ACCOUNT.test(c.ownerUsername || ''))
        .map((c) => mapInstagram(c, captions));
}

export async function collectLinkedIn({ input, lookbackDays, runActor }) {
    const items = await runActor(ACTORS.linkedin, {
        targetUrls: [input.linkedinCompanyUrl],
        maxPosts: input.maxPostsPerPage,
        postedLimit: linkedinPeriod(input.threadMaxAgeDays),
        scrapeComments: true,
        maxComments: input.maxCommentsPerPost,
        commentsPostedLimit: linkedinPeriod(Math.min(lookbackDays, 31)),
        scrapeReactions: false,
        includeReposts: false,
    });
    const postText = new Map(items.filter((i) => i.type === 'post').map((p) => [String(p.id), p.content]));
    return items
        .filter((i) => i.type === 'comment')
        .filter((c) => !c.actor?.author && !OWN_ACCOUNT.test(c.actor?.name || ''))
        .map((c) => mapLinkedIn(c, postText));
}

export const COLLECTORS = {
    app_store: collectAppStore,
    google_play: collectGooglePlay,
    reddit: collectReddit,
    facebook: collectFacebook,
    instagram: collectInstagram,
    linkedin: collectLinkedIn,
};
