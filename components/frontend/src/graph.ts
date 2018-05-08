import * as _ from 'lodash';

function reduction(acc, v) {
    let extension: object;
    if (acc === null) {
        extension = {}
    } else {
        extension = {
            children: [acc]
        }
    }

    const base = {
        token: v
    };

    return Object.assign({}, base, extension);
}

function stratifySentence(tokens: string[]) {
    return _.reduceRight(tokens, reduction, null);
}

export default { stratifySentence };
