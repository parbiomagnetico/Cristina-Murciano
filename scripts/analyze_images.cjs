const fs = require('fs');

const posts = JSON.parse(fs.readFileSync('src/data/posts.json', 'utf8'));

const imageCounts = {};
const noImage = [];
const duplicates = {};

posts.forEach(post => {
    const img = post.image;
    if (!img || img.trim() === '') {
        noImage.push(post.title);
    } else {
        imageCounts[img] = (imageCounts[img] || 0) + 1;
    }
});

Object.keys(imageCounts).forEach(img => {
    if (imageCounts[img] > 1) {
        duplicates[img] = imageCounts[img];
    }
});

console.log('--- RESUMEN DE IMÁGENES DEL BLOG ---');
console.log(`Total de artículos: ${posts.length}`);
console.log(`Artículos sin imagen: ${noImage.length}`);
if (noImage.length > 0) {
    console.log('Titulares sin imagen:', noImage);
}

const duplicateImgCount = Object.keys(duplicates).length;
console.log(`\nImágenes duplicadas (usadas en más de un post): ${duplicateImgCount}`);

if (duplicateImgCount > 0) {
    console.log('\nDetalle de duplicados:');
    Object.keys(duplicates).forEach(img => {
        const sharedBy = posts.filter(p => p.image === img).map(p => p.title);
        console.log(`- "${img}" se usa en ${duplicates[img]} posts:`);
        sharedBy.forEach(title => console.log(`    * ${title}`));
    });
}
