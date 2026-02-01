const fs = require('fs');

const stylePrompt = "premium high-key photography, clinical but warm atmosphere, minimalist composition, airy and ethereal feel, soft natural lighting, color palette of clean white, soft teal, and gentle lilac, soft ethereal light leaks, diffused holographic color washes in pastel magenta and teal, dreamy aura-like glow, female therapist dressed entirely in professional white, anonymous and faceless (face is NOT visible, head is cropped or turned away), focus is strictly on the treatment or the main subject, close-up shot of hands and skin, consistent minimalist treatment room with white walls and soft sheer curtains, 8k resolution, cinematic lighting, professional wellness aesthetic";
const negativePrompt = "--no sharp rainbow prisms, distinct rainbow lines, faces, facial features, eyes, looking at camera, gloves, latex gloves, medical gloves, surgical gloves, male therapist, dark gloomy atmosphere, neon, cyberpunk, low quality, cartoon, illustration, busy background, messy room, text, watermark, signature";

// Get user input from command line arguments
const args = process.argv.slice(2);
const subject = args.join(' ');

if (!subject) {
    console.error("❌ Error: Por favor proporciona una descripción del sujeto.");
    console.log("Uso: node scripts/generate_blog_prompt.js \"manos masajeando un pie\"");
    process.exit(1);
}

// Translate simple concepts if needed or just use as is (assuming user inputs English or we rely on model understanding)
// For best results, inputs should be in English, but models handle Spanish well. 
// We will construct the final string.

const finalPrompt = `${subject}, ${stylePrompt} ${negativePrompt}`;

console.log("\n✨ Prompt Generado (Copiar y Pegar):");
console.log("---------------------------------------------------");
console.log(finalPrompt);
console.log("---------------------------------------------------\n");
