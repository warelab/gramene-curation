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
  var fields = "g.gene_id,a.email,f.label as flag,c.pk as id,c.timestamp,fa.label as reason";
  var tables = "account a, curation c left join curation_to_flag_annotation ctfa on c.pk = ctfa.curation_pk left join flag_annotation fa on ctfa.flag_annotation_pk = fa.pk, gene g, flag f";
  var conditions  = "a.pk = c.account_pk and c.gene_pk = g.pk and c.flag_pk = f.pk and f.label != 'curate'";
  var params = {};
  if (req.swagger.params.since && req.swagger.params.since.value) {
    conditions += ` and c.timestamp >= '${req.swagger.params.since.value}'`;
    params.since = req.swagger.params.since.value;
  }
  if (req.swagger.params.until && req.swagger.params.until.value) {
    conditions += ` and c.timestamp <= '${req.swagger.params.until.value}'`;
    params.until = req.swagger.params.until.value;
  }
  var sql = `select ${fields} from ${tables} where ${conditions}`;
  client.query(sql, (err, pgres) => {
    if (err) {
      console.log(err.stack);
    }
    if (req.swagger.params.format && req.swagger.params.format.value === 'txt') {
      res.contentType('text/tab-separated-values');
      var transformer = csvStringify({header:true, delimiter: '\t', columns: ['gene','email','flag','reason']});
      var dTable = pgres.rows.map(r => [r.gene_id,r.email,r.flag,r.reason]);
      streamify(dTable).pipe(transformer).pipe(res);
    }
    else {
      res.json({
        header: {
          metadata: {
            params: params
          }
        },
        results: pgres.rows.map(r => {
          if (!r.reason) {
            delete r.reason; // delete null reason from response
          }
          return r;
        })
      });
    }
  })
}
