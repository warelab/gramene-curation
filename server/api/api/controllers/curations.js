'use strict';
var csvStringify = require('csv-stringify');
var streamify = require('stream-array');
/*
 'use strict' is not required but helpful for turning syntactical errors into true errors in the program flow
 https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
*/

/*
 Modules make it possible to import JavaScript files into your application.  Modules are imported
 using 'require' statements that give you a reference to the module.

  It is a good idea to list the modules that your application depends on in the package.json in the project root
 */
var util = require('util');
const { Client } = require('pg');
const client = new Client()

client.connect()

/*
 Once you 'require' a module you can reference the things that it exports.  These are defined in module.exports.

 For a controller in a127 (which this is) you should export the functions referenced in your Swagger document by name.

 Either:
  - The HTTP Verb of the corresponding operation (get, put, post, delete, etc)
  - Or the operationId associated with the operation in your Swagger document

  In the starter/skeleton project the 'get' operation on the '/hello' path has an operationId named 'hello'.  Here,
  we specify that in the exports of this module that 'hello' maps to the function named 'hello'
 */
module.exports = {
  curations: curations
};

/*
  Functions in a127 controllers used for operations should take two parameters:

  Param 1: a handle to the request object
  Param 2: a handle to the response object
 */
function curations(req, res) {
  // variables defined in the Swagger document can be referenced using req.swagger.params.{parameter_name}
/*
      - gene_id
      - email
      - flag
      - reason
      - timestamp
      - id
  
*/
  var fields = "g.gene_id,'suppressed@site.com' as email,f.label as flag,c.pk as id,c.timestamp,fa.label as reason";//",gt.tree_id,gt.set_id";`
  if (req.swagger.params.showEmail && req.swagger.params.showEmail.value) {
    fields = "g.gene_id,a.email,f.label as flag,c.pk as id,c.timestamp,fa.label as reason";//",gt.tree_id,gt.set_id";
//    console.error("showEmail is true?",req.swagger.params.showEmail);
  }
  var tables = "curation c"
  + " left join account a on c.account_pk = a.pk"
  + " left join curation_to_flag_annotation ctfa on c.pk = ctfa.curation_pk"
  + " left join flag_annotation fa on ctfa.flag_annotation_pk = fa.pk"
  + " left join gene g on c.gene_pk = g.pk"
  // + " left join gene_to_gene_tree gtgt on c.gene_pk = gtgt.gene_pk"
  // + " left join gene_tree gt on gtgt.gene_tree_pk = gt.pk"
  + " left join flag f on c.flag_pk = f.pk";
  var conditions  = "f.label != 'curate' and c.timestamp >= '2000-01-01'::date";
  var params = {};
  if (req.swagger.params.since && req.swagger.params.since.value) {
    conditions += ` and c.timestamp >= '${req.swagger.params.since.value}'::date`;
    params.since = req.swagger.params.since.value;
  }
  if (req.swagger.params.until && req.swagger.params.until.value) {
    conditions += ` and c.timestamp <= '${req.swagger.params.until.value}'::date`;
    params.until = req.swagger.params.until.value;
  }
  if (req.swagger.params.flagged && req.swagger.params.flagged.value) {
    conditions += " and f.label != 'okay'"
    params.flagged = true;
  }
  if (req.swagger.params.email && req.swagger.params.email.value) {
    conditions += ` and a.email like '%${req.swagger.params.email.value}%'`;
    params.email = req.swagger.params.email.value;
  }
  if (req.swagger.params.idList && req.swagger.params.idList.value) {
    function quotify(str) {
      return `'${str.split(',').join("','")}'`;
    }
    conditions += ` and g.gene_id IN (${quotify(req.swagger.params.idList.value)})`
    params.idList = req.swagger.params.idList.value;
  }
  var sql = `select ${fields} from ${tables} where ${conditions} order by c.timestamp`;
  // console.error(sql);
  client.query(sql, (err, pgres) => {
    if (err) {
      console.log(err.stack);
    }
    if (req.swagger.params.format && req.swagger.params.format.value === 'txt') {
      res.contentType('text/tab-separated-values');
      var transformer = csvStringify({header:true, delimiter: '\t', columns: ['gene_id','email','flag','reason','timestamp']});//,'tree_id','set_id']});
      const formatDate = timestamp => {
        var date = new Date(timestamp);
        return `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
      };
      var dTable = pgres.rows.map(r => [r.gene_id,r.email,r.flag,r.reason,formatDate(r.timestamp)]);//,r.tree_id,r.set_id]);
      streamify(dTable).pipe(transformer).pipe(res);
    }
    else {
      var rows = 1000000;
      if (req.swagger.params.rows && req.swagger.params.rows.value >=0) {
        rows = req.swagger.params.rows.value;
      }
      var minFlagged = 0;
      if (req.swagger.params.minFlagged && req.swagger.params.minFlagged.value > 0) {
        minFlagged = req.swagger.params.minFlagged.value;
      }
      let results = [];
      let geneTally = {}
      pgres.rows.forEach(r => {
        if (!r.reason) {
          delete r.reason; // delete null reason from response
        }
        if (!r.timestamp) {
          delete r.timestamp; // delete null timestamp
        }
        if (results.length < rows) {
          results.push(r);
        }
        if (!geneTally.hasOwnProperty(r.gene_id)) {
          geneTally[r.gene_id] = {
            flag: {},
            okay: {}
          }
        }
        if (geneTally[r.gene_id].hasOwnProperty(r.flag)) {
          geneTally[r.gene_id][r.flag][r.email] = 1;
        }
      });
      res.json({
        header: {
          metadata: {
            params: params
          }
        },
        results: results,
        genes: Object.keys(geneTally).map(gene_id => {
          let gt = geneTally[gene_id];
          return {
            gene_id: gene_id,
            okay: Object.keys(gt.okay).length,
            flagged: Object.keys(gt.flag).length
          }
        }).filter(g => g.flagged >= minFlagged)
      })
    }
  })
}
