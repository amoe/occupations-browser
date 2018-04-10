document.addEventListener('DOMContentLoaded', e => {
    sigma.parsers.json('data.json', {
        container: 'container',
        settings: {
            defaultNodeColor: '#ec5148'
        }
    })
});
