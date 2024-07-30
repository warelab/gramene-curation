#!/usr/bin/env node
const config = require('./config.json');
const _ = require("lodash");
const apiKey = config.API_KEY;

const spreadsheetId = '1-clhm1bgZW91cbYVd1iy-hye84GtBZ34QX4bXeEAOLw';
const range = 'Form Responses 1!A:L';

async function fetchData() {
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${range}?key=${apiKey}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    process(formatData(data.values));
  } catch (error) {
    console.error('error fetching data:', error);
  }
}

function formatData(rows) {
  if (rows.length === 0) return [];
  const keys = rows[0]; // First row as keys
  const formattedData = rows.slice(1).map(row => {
    let obj = {};
    keys.forEach((key, index) => {
      obj[key] = _.trim(row[index]) || null; // Assign values to keys, set null if undefined
    });
    return obj;
  });
  return formattedData;
}

function xxgroupBy(array, key) {
    return array.reduce((result, currentValue) => {
        // Get the value of the key we're grouping by
        const groupKey = currentValue[key];
        // If the key doesn't exist in the result object, create it
        if (!result[groupKey]) {
            result[groupKey] = [];
        }
        // Add the current value to the corresponding group
        result[groupKey].push(currentValue);
        return result;
    }, {}); // Initial value of the result object is an empty object
}

function uniq_case_insensitive(array) {
  const lowerCased = array.map(item => item.toLowerCase());
  const uniqLowerCased = _.uniq(lowerCased);

  const caseInsensitiveUniq = uniqLowerCased.map(lowerItem => 
    array.find(item => item.toLowerCase() === lowerItem)
  );
  return caseInsensitiveUniq;
}

const digitsRegex = /^\d+$/;
let res = [];
function process(entries) {
  const byGene = _.groupBy(entries, "Gene ID");
  Object.values(byGene).forEach(curations => {
    let gene = {
      locus: curations[0]['Gene ID'],
      gene_names: [],
      gene_symbols: [],
      references: {},
      po: [],
      to: []
    };
    curations.forEach(c => {
      if (c['Gene symbol used in publication']) {
        let symbol = c['Gene symbol used in publication'];
        if (symbol !== gene.locus) {
          if (symbol.indexOf(" ") !== -1) {
            gene.gene_names.push(symbol);
            console.error("symbol has spaces",gene.locus, symbol);
          } else {
            gene.gene_symbols.push(symbol)
          }
        }
      }
      if (c['Gene name used in publication']) {
        gene.gene_names.push(c['Gene name used in publication'])
      }
      if (!gene.references.hasOwnProperty(c['Literature Reference'])) {
        gene.references[c['Literature Reference']] = {
          description: c['Describe gene function'],
          literatureType: digitsRegex.test(c['Literature Reference']) ? 'PubMed' : 'DOI'
        }
      }
    });
    gene.gene_names = uniq_case_insensitive(gene.gene_names).join(', ');
    gene.gene_symbols = uniq_case_insensitive(gene.gene_symbols).join(', ');
    res.push(gene);
  });
  console.log(JSON.stringify(res,null,2));
}

fetchData();