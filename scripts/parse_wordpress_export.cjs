const fs = require('fs');
const path = require('path');

const inputFile = path.join(__dirname, '../export.xml');
const outputFile = path.join(__dirname, '../src/data/reviews.json');

fs.readFile(inputFile, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading XML file:', err);
        return;
    }

    console.log('File read successfully. Size:', data.length);

    // Regex to find all <item> blocks
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    const items = [];
    let match;

    while ((match = itemRegex.exec(data)) !== null) {
        items.push(match[1]);
    }

    // Find the raw item in 'items' whose title is Opiniones
    const opinionesItem = items.find(item => {
        const titleMatch = item.match(/<title>([\s\S]*?)<\/title>/);
        const title = titleMatch ? titleMatch[1] : '';
        return title.includes('Opiniones');
    });

    if (opinionesItem) {
        console.log('Found Opiniones page raw item! Extracting comments...');

        // Split by <wp:comment> tag for robustness
        const comments = opinionesItem.split('<wp:comment>').slice(1).map(c => c.split('</wp:comment>')[0]);

        const reviews = comments.map(c => {
            const extract = (tag) => {
                const regex = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`);
                const match = c.match(regex);
                if (match) {
                    // Remove CDATA if present
                    return match[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/, '$1').trim();
                }
                return '';
            };

            return {
                author: extract('wp:comment_author'),
                date: extract('wp:comment_date').split(' ')[0], // YYYY-MM-DD
                content: extract('wp:comment_content'),
                approved: extract('wp:comment_approved') === '1'
            };
        }).filter(r => r.approved && r.content);

        console.log(`Found ${reviews.length} approved reviews.`);

        fs.writeFileSync(outputFile, JSON.stringify(reviews, null, 4));
        console.log(`Successfully wrote reviews to ${outputFile}`);

    } else {
        console.log('Opiniones page raw item NOT found.');
    }
});
