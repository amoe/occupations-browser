import { Point } from './interfaces';

function getParentId(d) {
    return d.id.substring(0, d.id.lastIndexOf("."));
}

// Not sure what's happening here
function ourCompare(a, b) {
    return a.height - b.height || a.id.localeCompare(b.id);
}

// Projection function
function project(x, y) {
    var angle = (x - 90) / 180 * Math.PI, radius = y;
    return [radius * Math.cos(angle), radius * Math.sin(angle)];
}

function projectPoint(p: Point) {
    var angle = (p.x - 90) / 180 * Math.PI, radius = p.y;
    return {
        x: radius * Math.cos(angle),
        y: radius * Math.sin(angle)
    };
}

function isOnRightSide(node) {
    const isInFirstHalf = node.x < 180;
    const isLeafNode = !node.children;

    return isInFirstHalf == isLeafNode;
}

function formatPoint(point: Point) {
    const projected = projectPoint(point);

    return `${projected.x} ${projected.y}`;
}

// returns optimal bearing in radians
function bearing(point1: Point, point2: Point): number {
    var theta = Math.atan2(point2.x - point1.x, point1.y - point2.y);
    return theta;
}

// choose a concrete point that is on the optimal bearing of a source point
function getOptimalCircumferencePoint(
    sourcePoint: Point, sourceRadius: number, targetPoint: Point
): Point {
    const angle = (Math.PI * 1.5) + bearing(sourcePoint, targetPoint);

    console.log("angle was found as %o", angle);

    const x = sourcePoint.x + sourceRadius * Math.cos(angle);
    const y = sourcePoint.y + sourceRadius * Math.sin(angle);

    return { x, y };
}


function getPathDescriptionForEdge(sourcePoint: Point, sourceRadius: number, targetPoint: Point) {
    const circumferencePoint = getOptimalCircumferencePoint(sourcePoint, sourceRadius, targetPoint);

    console.log("found circumference point as %o", circumferencePoint);

    const moveInstruction = "M" + formatPoint(circumferencePoint);

    const controlStart = formatPoint({
        x: targetPoint.x,
        y: (targetPoint.y + circumferencePoint.y) / 2
    });

    const controlEnd = formatPoint({
        x: circumferencePoint.x,
        y: (targetPoint.y + circumferencePoint.y) / 2
    });

    const endPoint = formatPoint(targetPoint);

    const curveInstruction = `C ${controlStart}, ${controlEnd}, ${endPoint}`;
    const fullDescription = `${moveInstruction} ${curveInstruction}`;

    return fullDescription;
}


export default {
    getParentId, ourCompare, project, isOnRightSide, getPathDescriptionForEdge
};
