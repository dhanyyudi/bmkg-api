import { MAP } from './indonesia';

export type LatLon = [number, number];
export type XY = [number, number];

/** Place a coordinate on the map's SVG canvas. */
export function project(lat: number, lon: number): XY {
	return [(lon - MAP.lon0) * MAP.k, (MAP.lat0 - lat) * MAP.k];
}

const EARTH_RADIUS_KM = 6371;

export function distanceKm(a: LatLon, b: LatLon): number {
	const rad = Math.PI / 180;
	const dLat = (b[0] - a[0]) * rad;
	const dLon = (b[1] - a[1]) * rad;
	const h =
		Math.sin(dLat / 2) ** 2 + Math.cos(a[0] * rad) * Math.cos(b[0] * rad) * Math.sin(dLon / 2) ** 2;
	return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(h));
}

const same = (a: LatLon, b: LatLon) => Math.abs(a[0] - b[0]) < 1e-4 && Math.abs(a[1] - b[1]) < 1e-4;

/**
 * Split a warning area's flat coordinate list into closed rings.
 *
 * BMKG concatenates several rings into one array. A ring ends when a point
 * returns to the ring's start, or when the next point jumps more than 10 km.
 */
export function splitRings(coords: LatLon[] | null): LatLon[][] {
	if (!coords || coords.length < 3) return [];
	const rings: LatLon[][] = [];
	let start = coords[0];
	let ring: LatLon[] = [coords[0]];

	for (let i = 1; i < coords.length; i++) {
		const point = coords[i];

		if (ring.length >= 4 && distanceKm(ring[ring.length - 1], point) > 10) {
			rings.push([...ring, ring[0]]);
			start = point;
			ring = [point];
			continue;
		}

		ring.push(point);
		if (same(point, start) && ring.length >= 4) {
			rings.push(ring);
			ring = [];
			if (i + 1 < coords.length) {
				start = coords[i + 1];
				ring = [start];
				i++;
			}
		}
	}

	if (ring.length >= 4) rings.push([...ring, ring[0]]);
	return rings;
}

const MAX_EDGE_KM = 20;

/**
 * Rings worth drawing. Real boundaries are made of short edges; a ring with a
 * long edge is a strip artifact joining two distant clusters.
 */
export function warningRings(coords: LatLon[] | null): LatLon[][] {
	return splitRings(coords).filter((ring) => {
		for (let i = 0; i < ring.length - 1; i++) {
			if (distanceKm(ring[i], ring[i + 1]) > MAX_EDGE_KM) return false;
		}
		return true;
	});
}

export function ringPath(ring: LatLon[]): string {
	return `M${ring.map(([lat, lon]) => project(lat, lon).map((n) => n.toFixed(1)).join(',')).join('L')}Z`;
}

export interface Box {
	x: number;
	y: number;
	width: number;
	height: number;
}

/**
 * A viewBox around some points, padded to a given shape.
 *
 * `aspect` is width over height. The whole-country map is a wide strip; a
 * detail map can be taller, so it fills the panel it sits in.
 */
export function frame(points: LatLon[], minSpanDeg = 3, aspect = MAP.width / MAP.height): Box {
	const full: Box = { x: 0, y: 0, width: MAP.width, height: MAP.height };
	if (!points.length) return full;

	const xy = points.map(([lat, lon]) => project(lat, lon));
	let minX = Math.min(...xy.map((p) => p[0]));
	let maxX = Math.max(...xy.map((p) => p[0]));
	let minY = Math.min(...xy.map((p) => p[1]));
	let maxY = Math.max(...xy.map((p) => p[1]));

	let width = Math.max((maxX - minX) * 1.5, minSpanDeg * MAP.k);
	let height = Math.max((maxY - minY) * 1.5, (minSpanDeg * MAP.k) / aspect);
	if (width / height > aspect) height = width / aspect;
	else width = height * aspect;

	return { x: (minX + maxX) / 2 - width / 2, y: (minY + maxY) / 2 - height / 2, width, height };
}
