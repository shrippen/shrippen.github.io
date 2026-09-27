// Studio Weber demo world: helpers (appended to the data by demo/world.py build).
// Works in QML (.import "world.js" as World) and Node (require("./world.js")).
// Rules: today = DEMO_TODAY or the real date, anchor = Monday of today's week,
// date = anchor + offset days, text = value[lang] for {de, en} values.

function pad(n) { return (n < 10 ? "0" : "") + n; }

function parseDay(s) {
    var p = String(s).split("-");
    return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
}

function isoDate(d) {
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
}

// today(fixed): fixed is a Date, "YYYY-MM-DD" or empty. Node reads DEMO_TODAY itself.
function today(fixed) {
    if (!fixed && typeof process !== "undefined" && process.env && process.env.DEMO_TODAY)
        fixed = process.env.DEMO_TODAY;
    if (fixed instanceof Date) return new Date(fixed.getFullYear(), fixed.getMonth(), fixed.getDate());
    if (fixed) return parseDay(fixed);
    var n = new Date();
    return new Date(n.getFullYear(), n.getMonth(), n.getDate());
}

function anchor(day) {
    var d = today(day);
    d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
    return d;
}

// date(offset, fixedToday) -> Date at local midnight
function date(offset, fixedToday) {
    var d = anchor(fixedToday);
    d.setDate(d.getDate() + offset);
    return d;
}

// dateTime(offset, "HH:MM", fixedToday) -> Date
function dateTime(offset, hhmm, fixedToday) {
    var d = date(offset, fixedToday);
    var p = String(hhmm).split(":");
    d.setHours(Number(p[0]), Number(p[1]), 0, 0);
    return d;
}

function todayOffset(fixedToday) {
    return Math.round((today(fixedToday) - anchor(fixedToday)) / 86400000);
}

function t(value, lang) {
    if (value && typeof value === "object" && ("de" in value || "en" in value))
        return value[lang] || value.en || "";
    return value;
}

function byId(kind) {
    var out = {};
    var list = WORLD_DATA[kind];
    for (var i = 0; i < list.length; i++) out[list[i].id] = list[i];
    return out;
}

function minutes(hhmm) {
    var p = String(hhmm).split(":");
    return Number(p[0]) * 60 + Number(p[1]);
}

// Timesheets up to now (a Date), without rows that overlap a running timer.
function pastTimesheets(now, fixedToday) {
    now = now || new Date();
    var off = todayOffset(fixedToday);
    var nowMin = now.getHours() * 60 + now.getMinutes();
    var running = {};
    for (var r = 0; r < WORLD_DATA.running.length; r++)
        running[WORLD_DATA.running[r].user] = minutes(WORLD_DATA.running[r].start);
    var out = [];
    for (var i = 0; i < WORLD_DATA.timesheets.length; i++) {
        var row = WORLD_DATA.timesheets[i];
        if (row.day > off) continue;
        if (row.day === off) {
            var limit = running[row.user] !== undefined ? Math.min(running[row.user], nowMin) : nowMin;
            if (minutes(row.end) > limit) continue;
        }
        out.push(row);
    }
    return out;
}

var data = WORLD_DATA;

if (typeof module !== "undefined" && module.exports) {
    module.exports = { data: WORLD_DATA, today: today, anchor: anchor, date: date, dateTime: dateTime,
        todayOffset: todayOffset, isoDate: isoDate, t: t, byId: byId, minutes: minutes,
        pastTimesheets: pastTimesheets };
}
