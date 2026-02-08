const fs = require('fs');
const path = require('path');

const postsPath = path.join(__dirname, '../src/data/posts.json');
const blogDir = path.join(__dirname, '../src/content/blog');

const posts = JSON.parse(fs.readFileSync(postsPath, 'utf8'));

let updatedCount = 0;

posts.forEach(post => {
    const slug = post.slug;
    const jsonImage = post.image;

    const mdPath = path.join(blogDir, `${slug}.md`);

    if (fs.existsSync(mdPath)) {
        let content = fs.readFileSync(mdPath, 'utf8');

        // Regex to find the image field in frontmatter
        const imageRegex = /^image:\s*["']?([^"'\n]+)["']?/m;

        const match = content.match(imageRegex);

        if (match) {
            const currentImage = match[1];

            if (currentImage !== jsonImage) {
                console.log(`Updating ${slug}.md: ${currentImage} -> ${jsonImage}`);
                // Replace the line
                content = content.replace(imageRegex, `image: "${jsonImage}"`);
                fs.writeFileSync(mdPath, content, 'utf8');
                updatedCount++;
            }
        } else {
            // Add image field if missing (after date, or title)
            // simplified approach: append to frontmatter start
            // creating logic is complex if frontmatter is messy, skipping for now
            console.log(`⚠️ No image field found in ${slug}.md`);
        }
    } else {
        console.log(`❌ Markdown file for ${slug} not found.`);
    }
});

console.log(`\nSync complete. Updated ${updatedCount} files.`);
