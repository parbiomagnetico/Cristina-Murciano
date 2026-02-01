
const fs = require('fs');
const path = require('path');

const postsPath = path.join(__dirname, '../src/data/posts.json');
const posts = JSON.parse(fs.readFileSync(postsPath, 'utf8'));

// Exact mappings for the unique images we generated
const uniqueMapping = {
    'contracturas': { image: 'blog-contracturas.png', alt: 'Ilustración detallada de la musculatura de la espalda mostrando contracturas y puntos de tensión' },
    'circulacion': { image: 'blog-circulacion.png', alt: 'Diagrama del sistema circulatorio en las piernas mostrando el retorno venoso' },
    'efectos-masaje-circulatorio': { image: 'blog-efectos-masaje-circulatorio.png', alt: 'Beneficios del masaje circulatorio: alivio de pesadez y mejora del flujo sanguíneo' },
    'cuidar-cuerpo': { image: 'blog-cuidar-cuerpo.png', alt: 'Mujer cuidando su cuerpo y bienestar en un entorno natural y relajante' },
    'tratar-sobrecarga-muscular': { image: 'blog-tratar-sobrecarga-muscular.png', alt: 'Terapeuta tratando una sobrecarga muscular en la zona cervical y hombros' },
    'ejercicios-relajacion': { image: 'blog-ejercicios-relajacion.png', alt: 'Mujer practicando ejercicios de respiración y relajación al aire libre' },
    'fisioterapia-deportiva': { image: 'blog-physio-deportiva.png', alt: 'Masaje terapéutico deportivo para recuperación muscular en pierna' },
    'habitos-saludables': { image: 'blog-habitos-saludables.png', alt: 'Vida saludable: hidratación, alimentación natural y yoga' },
    'presoterapia': { image: 'blog-presoterapia.png', alt: 'Tratamiento de presoterapia profesional para activar la circulación' },
    'cuidar-piel': { image: 'blog-cuidar-piel.png', alt: 'Aplicación de crema hidratante y cuidado de la piel en sesión de bienestar' },
    'tendinitis': { image: 'blog-tendinitis.png', alt: 'Tratamiento específico de fisioterapia para tendinitis de hombro' }
};

// Keyword fallback for the rest (using themed images)
const themeMapping = [
    { image: 'blog-massage.png', alt: 'Terapeuta realizando un masaje terapéutico en la espalda para aliviar dolor y tensión', keywords: ['masaje', 'dolor', 'espalda', 'contractura', 'lumbar', 'antiestres', 'tensión'] },
    { image: 'blog-legs.png', alt: 'Tratamiento de piernas cansadas y circulación, masajeando desde los tobillos hacia arriba', keywords: ['piernas', 'circulación', 'presoterapia', 'tacones', 'varices'] },
    { image: 'blog-reflexology.png', alt: 'Sesión de reflexología podal, estimulando puntos reflejos en la planta del pie', keywords: ['reflex', 'pies', 'metamorfico'] },
    { image: 'blog-aroma.png', alt: 'Aceites esenciales y aromaterapia para masaje relajante y bienestar emocional', keywords: ['aroma', 'esencial', 'aceite'] },
    { image: 'blog-head.png', alt: 'Masaje craneal y facial para aliviar migrañas y tensión cervical', keywords: ['cabeza', 'craneal', 'facial', 'cefalea', 'migraña'] },
    { image: 'blog-stones.png', alt: 'Piedras volcánicas calientes colocadas sobre la espalda para terapia geotermal', keywords: ['piedras', 'geotermal', 'volcán'] },
    { image: 'blog-bamboo.png', alt: 'Terapia con cañas de bambú para masaje vigorizante y drenante', keywords: ['bambu', 'cañas'] },
    { image: 'blog-physio.png', alt: 'Fisioterapia y vendaje neuromuscular para tratamiento de lesiones deportivas', keywords: ['fisioterapia', 'esguince', 'vendaje', 'kinesio', 'lesion', 'deportiva', 'tendinitis', 'osteoartritis'] },
    { image: 'blog-water.png', alt: 'Vaso de agua pura, simbolizando la hidratación y salud renal', keywords: ['agua', 'hidro', 'beber'] },
    { image: 'blog-hands.png', alt: 'Cuidado y masaje de manos, aliviando tensión en muñecas y dedos', keywords: ['manos'] },
    { image: 'blog-lifestyle.png', alt: 'Estilo de vida saludable, equilibrio cuerpo-mente y bienestar natural', keywords: ['postura', 'habitos', 'estiramientos', 'salud', 'cuerpo', 'vida'] }
];

let updatedCount = 0;

posts.forEach(post => {
    // 1. Check if we have a unique image for this slug
    if (uniqueMapping[post.slug]) {
        post.image = uniqueMapping[post.slug].image;
        post.image_alt = uniqueMapping[post.slug].alt;
        updatedCount++;
    } else {
        // 2. Fallback to theme matching
        // Only update if image matches fallback to avoid overwriting manually assigned images if any (though currently we are overwriting all)
        // Actually, let's keep the logic simple: overwrite to ensure consistency given we are generating alt tags now.

        const text = (post.slug + ' ' + post.title + ' ' + post.excerpt).toLowerCase();
        const match = themeMapping.find(m => m.keywords.some(k => text.includes(k)));

        if (match) {
            post.image = match.image;
            post.image_alt = match.alt;
        } else {
            post.image = 'blog-lifestyle.png'; // Ultimate fallback
            post.image_alt = 'Vida saludable y bienestar natural';
        }
    }
});

fs.writeFileSync(postsPath, JSON.stringify(posts, null, 4));
console.log(`Scripts finished. Updated image assignments.`);
