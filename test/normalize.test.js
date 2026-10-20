import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
    finalize, isEmojiOnly, mapAppStore, mapGooglePlay, mapReddit, redditPostId, relevantRedditThreads, toIsoDate,
} from '../src/normalize.js';

const FIELDS = ['source', 'id', 'date', 'text', 'rating', 'context', 'url'];

test('isEmojiOnly catches emoji, flags, joiners and punctuation only', () => {
    for (const text of ['💙', '😆😆', '👍🏽', '🇨🇿 👌', '❤️‍🔥!!', '  🙂 ', '...']) {
        assert.equal(isEmojiOnly(text), true, text);
    }
    for (const text of ['Real', 'Super 💙', '5', 'Tak vstanu a budu hledat s ním 😂']) {
        assert.equal(isEmojiOnly(text), false, text);
    }
});

test('App Store review keeps only the agreed fields and merges title with text', () => {
    const r = mapAppStore({
        id: '14664762959', date: '2026-10-14T00:00:00.000Z', userName: 'someone', userUrl: 'https://x/u',
        version: '26.34.27', score: 5, title: 'Super apka', text: 'Vývojáři naslouchají', url: 'https://itunes.apple.com/us/review',
    }, { appId: '1163368801', country: 'cz' });
    assert.deepEqual(Object.keys(r), FIELDS);
    assert.equal(r.id, 'app_store:14664762959');
    assert.equal(r.text, 'Super apka\nVývojáři naslouchají');
    assert.equal(r.rating, 5);
    assert.equal(r.context, 'App version 26.34.27');
    assert.ok(!JSON.stringify(r).includes('someone'));
});

test('toIsoDate handles second and millisecond timestamps and Reddit offsets', () => {
    assert.equal(toIsoDate(1792143314), '2026-10-16T09:35:14.000Z');
    assert.equal(toIsoDate(1792143314000), '2026-10-16T09:35:14.000Z');
    assert.equal(toIsoDate('2026-10-01T05:36:07.000000+0000'), '2026-10-01T05:36:07.000Z');
    assert.equal(toIsoDate('2026-10-16'), '2026-10-16T00:00:00.000Z');
    assert.equal(toIsoDate('nonsense'), null);
});

test('App Store review does not repeat a title equal to the text', () => {
    const r = mapAppStore({ id: '1', date: '2026-10-18', score: 5, title: 'Super', text: 'Super' }, { appId: '1', country: 'cz' });
    assert.equal(r.text, 'Super');
});

test('Google Play review drops reviewer and links to the review', () => {
    const r = mapGooglePlay({
        reviewId: 'abc', rating: 3, reviewer: 'Jan Novák', userImage: 'https://img', date: '2026-10-13',
        appVersion: '26.34.14', body: 'Nelze se přihlásit', helpfulCounts: 29,
    }, { appId: 'cz.csas.georgego' });
    assert.deepEqual(Object.keys(r), FIELDS);
    assert.equal(r.url, 'https://play.google.com/store/apps/details?id=cz.csas.georgego&reviewId=abc');
    assert.ok(!JSON.stringify(r).includes('Novák'));
});

const redditRows = [
    { _type: 'post', id: '1wwn4bc', subreddit: 'czech', title: 'Dotaz', selftext: 'George píše že musím na pobočku', createdAt: '2026-10-03T13:20:41.000000+0000', permalink: '/r/czech/comments/1wwn4bc/dotaz/', author: 'u1' },
    { _type: 'comment', id: 't1_a', subreddit: 'czech', postTitle: 'Dotaz', body: 'Domluv se s bankerem', createdAt: '2026-10-03T13:44:46.142000+0000', permalink: '/r/czech/comments/1wwn4bc/dotaz/a/', author: 'u2' },
    { _type: 'post', id: '1uveyk7', subreddit: 'Witcher3', title: 'I got lucky!', selftext: 'There was a competition in my bank', createdAt: '2026-07-13T15:35:13.000000+0000', permalink: '/r/Witcher3/comments/1uveyk7/i_got_lucky/' },
    { _type: 'comment', id: 't1_b', subreddit: 'Witcher3', postTitle: 'I got lucky!', body: 'Zaklinać', createdAt: '2026-07-13T16:02:26.763000+0000', permalink: '/r/Witcher3/comments/1uveyk7/i_got_lucky/b/' },
    { _type: 'post', id: '1x', subreddit: 'eupersonalfinance', title: 'Česká spořitelna Level Up?', selftext: '', createdAt: '2026-10-01T00:00:00.000000+0000', permalink: '/r/eupersonalfinance/comments/1x/cs/' },
    { _type: 'post', id: '1y', subreddit: 'europe', title: 'ČS raised fees', selftext: '', createdAt: '2026-10-01T00:00:00.000000+0000', permalink: '/r/europe/comments/1y/cs/' },
];

test('Reddit keeps Czech subreddits and threads naming the bank, drops the rest', () => {
    const relevant = relevantRedditThreads(redditRows, ['czech', 'Prague']);
    assert.deepEqual([...relevant].sort(), ['1wwn4bc', '1x', '1y']);
    assert.equal(redditPostId(redditRows[1]), '1wwn4bc');
});

test('Reddit post and comment mapping', () => {
    const post = mapReddit(redditRows[0]);
    assert.equal(post.text, 'Dotaz\n\nGeorge píše že musím na pobočku');
    assert.equal(post.context, 'r/czech');
    assert.equal(post.date, '2026-10-03T13:20:41.000Z');
    const comment = mapReddit(redditRows[1]);
    assert.equal(comment.context, 'r/czech: Dotaz');
    assert.equal(comment.url, 'https://www.reddit.com/r/czech/comments/1wwn4bc/dotaz/a/');
    assert.ok(!JSON.stringify(comment).includes('u2'));
    assert.equal(mapReddit({ ...redditRows[1], body: '[deleted]' }), null);
});

test('finalize filters by window, emoji, empties and duplicates', () => {
    const base = { source: 'instagram', rating: null, context: 'post', url: null };
    const { records, stats } = finalize([
        { ...base, id: 'instagram:1', date: '2026-10-17T12:00:00.000Z', text: 'Přesně tak' },
        { ...base, id: 'instagram:2', date: '2026-10-17T12:01:00.000Z', text: '😆😆' },
        { ...base, id: 'instagram:3', date: '2026-09-01T00:00:00.000Z', text: 'old' },
        { ...base, id: 'instagram:1', date: '2026-10-17T12:00:00.000Z', text: 'Přesně tak' },
        { ...base, id: 'instagram:4', date: '2026-10-18T12:00:00.000Z', text: 'Přesně tak' },
        { ...base, id: 'instagram:5', date: '2026-10-19T12:00:00.000Z', text: '' },
        null,
    ], { since: new Date('2026-10-12T00:00:00Z'), until: new Date('2026-10-20T00:00:00Z') });
    assert.deepEqual(records.map((r) => r.id), ['instagram:1']);
    assert.deepEqual(stats, { empty: 1, emojiOnly: 1, outsideWindow: 1, duplicate: 2 });
});
