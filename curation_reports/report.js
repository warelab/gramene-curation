#!/usr/bin/env node
const fetch = require('node-fetch');
const _ = require('lodash');
const url = 'http://devdata.gramene.org/curation/curations?since=2020-03-10';

function getReason(r) {
  switch (r) {
  case 'gain5':
    return 'G__'
  case 'gainAA':
    return '_G_'
  case 'gain3':
    return '__G'
  case 'loss5':
    return 'L__'
  case 'lossAA':
    return '_L_'
  case 'loss3':
    return '__L'
  default:
    return r
  }
}

function uniqify(a) {
  let o = {};
  a.forEach(x => o[x]=1);
  return Object.keys(o);
}
fetch(url)
.then(res => res.json())
.then(json => {
  const curations = json.results;
  console.log(`curations\t${curations.length}`);
  let genes={};
  let reasonFrequency={};
  let emailFrequency={};
  curations.forEach(c => {
    if (c.reason !== 'other' || true) {
      if (!genes.hasOwnProperty(c.gene_id)) {
        genes[c.gene_id] = {
          okay:[],
          flag:[],
          reasons:[]
        }
      }
      if (!emailFrequency.hasOwnProperty(c.email)) {
        emailFrequency[c.email]=0;
      }
      emailFrequency[c.email]++;
      if (c.flag === 'okay') {
        genes[c.gene_id].okay.push(c.email)
      }
      else {
        genes[c.gene_id].flag.push(c.email);
        const reason = getReason(c.reason);
        if (!reasonFrequency.hasOwnProperty(reason)) {
          reasonFrequency[reason]=0;
        }
        reasonFrequency[reason]++;
        genes[c.gene_id].reasons.push(reason);
      }
    }
  });
  
  let n_flagged=0;
  let n_flagged_twice=0;
  const glist = Object.keys(genes);
  glist.forEach(g => {
    const gene = genes[g];
    if (gene.flag.length > 0) {
      n_flagged++;
      if (gene.flag.length > 1) {
        console.log(g,_.uniq(gene.reasons).join(','),"FLAGGED_TWICE");
        n_flagged_twice++;
      }
    }
  });
  console.log(`curators\t${Object.keys(emailFrequency).length}`);
  Object.keys(emailFrequency).sort((a,b)=>emailFrequency[b]-emailFrequency[a]).forEach(ef => {
    console.log(`${ef}\t${emailFrequency[ef]}`);
  });
  console.log(`genes\t${glist.length}`);
  console.log(`flagged\t${n_flagged}`);
  console.log(`flagged twice\t${n_flagged_twice}`);
  Object.keys(reasonFrequency).sort((a,b)=>reasonFrequency[b]-reasonFrequency[a]).forEach(rf => {  
    console.log(`${rf}\t${reasonFrequency[rf]}`);
  });
});
