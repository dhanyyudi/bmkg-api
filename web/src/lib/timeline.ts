import type { Earthquake } from './api';
import { parseTime } from './format';

/** The period a set of earthquakes covers, ending now. */
export interface Timeline {
	origin: number;
	span: number;
}

export function timelineOf(quakes: Earthquake[], now: number = Date.now()): Timeline {
	const times = quakes.map((q) => parseTime(q.datetime).getTime());
	const start = times.length ? Math.min(...times) : now - 86_400_000;
	// A little room after the newest event, so its burst is not cut off.
	const span = Math.max(now - start, 3_600_000) * 1.04;
	return { origin: now - span, span };
}

/** Where an earthquake sits on the timeline, from 0 (oldest) to 1 (now). */
export function fractionOf(quake: Earthquake, timeline: Timeline): number {
	return (parseTime(quake.datetime).getTime() - timeline.origin) / timeline.span;
}

/** The banner replays the period in this many milliseconds. */
export const REPLAY_MS = 2600;
export const REPLAY_DELAY_MS = 300;
