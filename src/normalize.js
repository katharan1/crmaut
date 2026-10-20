// Pure helpers that turn raw scraper rows into Customer Insights records.
// Every record has exactly these fields - author names, profile links and
// pictures are never copied over:
//   source, id, date, text, rating, context, url

export const SOURCES = ['app_store', 'google_play', 'reddit', 'facebook', 'instagram', 'linkedin'];

const CONTEXT_MAX_LENGTH = 300;

// Characters that carry no words: emoji, skin tones, joiners, variation selectors,
// regional indicators (flags), punctuation, symbols and whitespace.
const NON_WORD_CHARS = /[\p{Extended_Pictographic}\p{Emoji_Modifier}\p{Regional_Indicator}‍︎️⃣\p{P}\p{S}\s]/gu;

export function isEmojiOnly(text) {
    return typeof text === 'string' && text.replace(NON_WORD_CHARS, '').length === 0;
}

export function truncate(text, max = CONTEXT_MAX_LENGTH) {
    if (!text) return null;
    const clean = String(text).replace(/\s+/g, ' ').trim();
    if (!clean) return null;
    return clean.length > max ? `${clean.slice(0, max - 1)}…` : clean;
}

export function toIsoDate(value) {
    if (value === null || value === undefined || value === '') return null;
    // Numeric timestamps come in seconds (Google Play, Reddit) or milliseconds (LinkedIn).
    const date = typeof value === 'number'
        ? new Date(value < 1e12 ? value * 1000 : value)
        : new Date(String(value).replace(/\+0000$/, 'Z'));
    return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

function record({ source, id, date, text, rating = null, context = null, url = null }) {
    return {
        source,
        id: `${source}:${id}`,
        date: toIsoDate(date),
        text: typeof text === 'string' ? text.trim() : '',
        rating: rating === null || rating === undefined ? null : Number(rating),
        context: truncate(context),
        url: url || null,
    };
}

// ---------- App Store (thewolves/appstore-reviews-scraper) ----------

export function mapAppStore(item, { appId, country }) {
    const title = (item.title || '').trim();
    const body = (item.text || '').trim();
    // Short reviews often repeat the title as the body ("Super" / "Super").
    const text = title && body && title !== body ? `${title}\n${body}` : body || title;
    return record({
        source: 'app_store',
        id: item.id,
        date: item.date,
        text,
        rating: item.score,
        context: item.version ? `App version ${item.version}` : null,
        url: `https://apps.apple.com/${country}/app/id${appId}?see-all=reviews`,
    });
}

// ---------- Google Play (neatrat/google-play-store-reviews-scraper) ----------

export function mapGooglePlay(item, { appId }) {
    return record({
        source: 'google_play',
        id: item.reviewId,
        date: item.timestamp || item.date,
        text: item.body,
        rating: item.rating,
        context: item.appVersion ? `App version ${item.appVersion}` : null,
        url: `https://play.google.com/store/apps/details?id=${appId}&reviewId=${item.reviewId}`,
    });
}

// ---------- Reddit (clearpath/reddit-post-comments-bulk-scraper) ----------

// Mentions that clearly mean Česká spořitelna, with or without diacritics.
const BRAND_PATTERN = /spořiteln|sporiteln|(?<!\p{L})(?:csas|čs|spořk[auyo])(?!\p{L})/iu;
const REMOVED_BODIES = new Set(['[deleted]', '[removed]']);

export function redditPostId(item) {
    if (item._type === 'post') return String(item.id).replace(/^t3_/, '');
    const match = /\/comments\/([a-z0-9]+)\//i.exec(item.permalink || '');
    return match ? match[1] : (item._post_id ? String(item._post_id).replace(/^t3_/, '') : null);
}

// A thread is kept when it lives in a Czech subreddit, or when the post itself
// names the bank. This drops search hits like r/Witcher3 threads that only
// matched on an image or a link. Comments inherit the decision of their thread,
// because replies rarely repeat the bank's name.
export function relevantRedditThreads(items, czechSubreddits) {
    const czech = new Set(czechSubreddits.map((s) => s.toLowerCase().replace(/^r\//, '')));
    const relevant = new Set();
    for (const item of items) {
        if (item._type !== 'post') continue;
        const inCzechSub = czech.has(String(item.subreddit || '').toLowerCase());
        const mentionsBrand = BRAND_PATTERN.test(`${item.title || ''}\n${item.selftext || ''}`);
        if (inCzechSub || mentionsBrand) relevant.add(redditPostId(item));
    }
    return relevant;
}

export function mapReddit(item) {
    const isPost = item._type === 'post';
    const text = isPost ? [item.title, item.selftext].filter(Boolean).join('\n\n') : item.body;
    if (!isPost && REMOVED_BODIES.has(String(text).trim())) return null;
    const subreddit = item.subreddit ? `r/${item.subreddit}` : null;
    return record({
        source: 'reddit',
        id: item.id,
        date: item.createdAt || item.created_utc,
        text,
        context: isPost ? subreddit : [subreddit, item.postTitle].filter(Boolean).join(': '),
        url: item.permalink ? `https://www.reddit.com${item.permalink}` : item.url,
    });
}

// ---------- Facebook (apify/facebook-comments-scraper) ----------

export function mapFacebook(item) {
    return record({
        source: 'facebook',
        id: item.commentId || item.id,
        date: item.date,
        text: item.text,
        context: item.postTitle,
        url: item.commentUrl,
    });
}

// ---------- Instagram (apify/instagram-comment-scraper) ----------

export function mapInstagram(item, captionsByPostUrl) {
    return record({
        source: 'instagram',
        id: item.id,
        date: item.timestamp,
        text: item.text,
        context: captionsByPostUrl.get(normalizeInstagramUrl(item.postUrl)) || null,
        url: item.commentUrl,
    });
}

export function normalizeInstagramUrl(url) {
    const match = /instagram\.com\/(?:[^/]+\/)?(p|reel)\/([^/?#]+)/i.exec(url || '');
    return match ? `${match[1].toLowerCase()}/${match[2]}` : url;
}

// ---------- LinkedIn (harvestapi/linkedin-company-posts) ----------

export function mapLinkedIn(item, postTextById) {
    return record({
        source: 'linkedin',
        id: item.id,
        date: item.createdAt || item.createdAtTimestamp,
        text: item.commentary,
        context: postTextById.get(String(item.postId)) || null,
        url: item.linkedinUrl,
    });
}

// ---------- Shared filtering ----------

// Drops empty and emoji-only texts, items outside the date window, and repeats.
// Repeats are the same id, or the same text posted twice in the same place
// (people double-submit comments).
export function finalize(records, { since, until = new Date(), dropEmojiOnly = true }) {
    const out = [];
    const seenIds = new Set();
    const seenTexts = new Set();
    const stats = { empty: 0, emojiOnly: 0, outsideWindow: 0, duplicate: 0 };
    for (const r of records) {
        if (!r) continue;
        if (!r.text) { stats.empty++; continue; }
        if (dropEmojiOnly && isEmojiOnly(r.text)) { stats.emojiOnly++; continue; }
        const time = r.date ? new Date(r.date).getTime() : NaN;
        if (Number.isNaN(time) || time < since.getTime() || time > until.getTime()) { stats.outsideWindow++; continue; }
        const textKey = `${r.source}|${r.context}|${r.text}`;
        if (seenIds.has(r.id) || seenTexts.has(textKey)) { stats.duplicate++; continue; }
        seenIds.add(r.id);
        seenTexts.add(textKey);
        out.push(r);
    }
    out.sort((a, b) => b.date.localeCompare(a.date));
    return { records: out, stats };
}
