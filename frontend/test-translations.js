// Test the translation routing functionality
import { getTranslatedPath, getCanonicalPath } from '../lib/i18n';

console.log('Testing translated paths:');

// Test categories paths
console.log('EN categories:', getTranslatedPath('categories', 'en')); // should be 'categories'
console.log('PT categories:', getTranslatedPath('categories', 'pt')); // should be 'categorias'  
console.log('NL categories:', getTranslatedPath('categories', 'nl')); // should be 'categorieen'

// Test businesses paths
console.log('EN businesses:', getTranslatedPath('businesses', 'en')); // should be 'businesses'
console.log('PT businesses:', getTranslatedPath('businesses', 'pt')); // should be 'empresas'
console.log('NL businesses:', getTranslatedPath('businesses', 'nl')); // should be 'bedrijven'

// Test reverse mapping
console.log('Canonical categorias:', getCanonicalPath('categorias')); // should be 'categories'
console.log('Canonical categorieen:', getCanonicalPath('categorieen')); // should be 'categories'
console.log('Canonical empresas:', getCanonicalPath('empresas')); // should be 'businesses'
console.log('Canonical bedrijven:', getCanonicalPath('bedrijven')); // should be 'businesses'