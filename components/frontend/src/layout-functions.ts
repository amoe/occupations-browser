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

function isOnRightSide(node) {
    const isInFirstHalf = node.x < 180;
    const isLeafNode = !node.children;

    return isInFirstHalf == isLeafNode;
}

export default {
    getParentId, ourCompare, project, isOnRightSide
};
