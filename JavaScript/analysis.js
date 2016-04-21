var esprima = require("esprima");
var options = { tokens: true, tolerant: true, loc: true, range: true, comment: true };
var fs = require("fs");
var female = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\Female';
var male = 'C:\\Users\\wddlz\\Documents\\GitHub\\CSC720\\Files\\Male';
var imports = 0;
var literals = 0;
var identifiers = 0;
var vars = 0;
var functions = 0;
var decisions = 0;
var size = 0; // esprima does not count trailing comments as lines contributing to the end of the program, this differs from the python program.
// arrays that hold function specific values. 
// maximum holds the highest values for each of the 5 function specific values 
// cumulative holds the values of each function added together
var maximum = { scc: 0, mnd: 0, mc: 0, p: 0, l: 0 };
var cumulative = { scc: 0, mnd: 0, mc: 0, p: 0, l: 0 };
function main() {
    var maleFiles = fs.readdirSync(male);
    var femaleFiles = fs.readdirSync(female);

    // for (f in maleFiles) {
    //     console.log(maleFiles[f]);
    // }
    // for (f in femaleFiles) {
    //     console.log(femaleFiles[f]);
    // }

    /*
     * Remove single processing in favor of batch (directory) processing  
     */
    // var args = process.argv.slice(2);

    // if (args.length == 0) 
    // {
    //     args = ["analysis.js"];
    // }
    // var filePath = args[0];

    // !important TODO flip these depending on which gender category is being ran
    /* FLIP MALE */
    // for (f in maleFiles) {
    //     process(male + '\\', maleFiles[f]);
    // }
    /* END FLIP */

    /* FLIP FEMALE */
    for (f in femaleFiles) {
        process(female + '\\', femaleFiles[f]);
    }
    /* END FLIP */
}

function process(d, f) {
    console.log('file:'  + d + f);
    // reset values for new file being proccessed
    imports = 0;
    literals = 0;
    identifiers = 0;
    vars = 0;
    functions = 0;
    decisions = 0;
    size = 0;
    maximum = { scc: 0, mnd: 0, mc: 0, p: 0, l: 0 };
    cumulative = { scc: 0, mnd: 0, mc: 0, p: 0, l: 0 };
    builders = {};
    
    complexity(d + f);

    // Report
    for (var node in builders) {
        var builder = builders[node];
        builder.report();

        // set result arrays
        if (maximum.scc < builder.SimpleCyclomaticComplexity) {
            maximum.scc = builder.SimpleCyclomaticComplexity;
        }
        if (maximum.mnd < builder.MaxNestingDepth) {
            maximum.mnd = builder.MaxNestingDepth;
        }
        if (maximum.mc < builder.MaxConditions) {
            maximum.mc = builder.MaxConditions;
        }
        if (maximum.p < builder.ParameterCount) {
            maximum.p = builder.ParameterCount;
        }
        if (maximum.l < (builder.StopLine - builder.StartLine)) {
            maximum.l = (builder.StopLine - builder.StartLine);
        }

        cumulative.scc += builder.SimpleCyclomaticComplexity;
        cumulative.mnd += builder.MaxNestingDepth;
        cumulative.mc += builder.MaxConditions;
        cumulative.p += builder.ParameterCount;
        cumulative.l += (builder.StopLine - builder.StartLine);

    }
    console.log('PROG: Imports, Functions, Literals, Identifiers, Vars, Decisions, Size || MAX(func): CyclComp, NestDepth, MaxConde, Params, Size || CUMULATIVEMAX(func): CyclComp, NestDepth, MaxConde, Params, Size');
    console.log(('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}').format(imports, functions, literals, identifiers, vars, decisions, size,
        maximum.scc, maximum.mnd, maximum.mc, maximum.p, maximum.l, cumulative.scc, cumulative.mnd, cumulative.mc, cumulative.p, cumulative.l));
        
    var fname = 'temp';
    if (d == male + '\\') {
        fname = 'm_';
    } else if (d == female + '\\') {
        fname = 'f_';
    }
    
    fs.appendFile(fname + f + '_res.txt', 
        ('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}')
        .format(imports, functions, literals, identifiers, vars, decisions, size, 
            maximum.scc, maximum.mnd, maximum.mc, maximum.p, maximum.l, cumulative.scc, cumulative.mnd, cumulative.mc, cumulative.p, cumulative.l), 
        function (err) { 
            if (err) throw err;
            console.log('Data appended to file');
        });
}
var builders = {};

// Represent a reusable "class" following the Builder pattern.
function ComplexityBuilder() {
    this.StartLine = 0; // done
    this.StopLine = 0; // done
    this.FunctionName = ""; // done
    // The number of parameters for functions
    this.ParameterCount = 0; // done
    // Number of if statements/loops + 1
    this.SimpleCyclomaticComplexity = 0;
    // The max depth of scopes (nested ifs, loops, etc)
    this.MaxNestingDepth = 0; // done
    // The max number of conditions in one decision statement.
    this.MaxConditions = 0; // done

    this.report = function () {
        console.log(
            (
                "{0}(): {1} to {6}\n" +
                "============\n" +
                "SimpleCyclomaticComplexity: {2}\t" +
                "MaxNestingDepth: {3}\t" +
                "MaxConditions: {4}\t" +
                "Parameters: {5}\t" +
                "Size: {7}\n\n"
                )
            .format(this.FunctionName, this.StartLine,
                this.SimpleCyclomaticComplexity, this.MaxNestingDepth,
                this.MaxConditions, this.ParameterCount, this.StopLine, this.StopLine - this.StartLine)
            );
    }
}

// A function following the Visitor pattern. Provide current node to visit and function that is evaluated at each node.
function traverse(object, visitor) {
    var key, child;
    visitor.call(null, object);
    for (key in object) {
        if (object.hasOwnProperty(key)) {
            child = object[key];
            if (typeof child === 'object' && child !== null) {
                traverse(child, visitor);
            }
        }
    }
}

// A function following the Visitor pattern.
// Annotates nodes with parent objects.
function traverseWithParents(object, visitor) {
    var key, child;
    visitor.call(null, object);
    for (key in object) {
        if (object.hasOwnProperty(key)) {
            child = object[key];
            if (typeof child === 'object' && child !== null && key != 'parent') {
                child.parent = object;
                traverseWithParents(child, visitor);
            }
        }
    }
}


// A function following the Visitor pattern but allows canceling transversal if visitor returns false.
function traverseWithCancel(object, visitor) {
    var key, child;
    if (visitor.call(null, object)) {
        for (key in object) {
            if (object.hasOwnProperty(key)) {
                child = object[key];
                if (typeof child === 'object' && child !== null) {
                    traverseWithCancel(child, visitor);
                }
            }
        }
    }
}

function complexity(filePath) {
    var buf = fs.readFileSync(filePath, "utf8");
    var ast = esprima.parse(buf, options);
    // Tranverse program with a function visitor.
    traverseWithParents(ast, function (node) {
        if (node.type === 'Program') {
            size = node.loc.end.line;
            console.log('File size: ' + size);
        } else if (node.type === 'FunctionDeclaration') { 
            var builder = new ComplexityBuilder();
            functions += 1;
            builder.FunctionName = functionName(node);
            builder.ParameterCount = getParameters(node);
            builder.StartLine = node.loc.start.line;
            builder.StopLine = node.loc.end.line;
            builder.SimpleCyclomaticComplexity = getCyclomaticComplexity(node);
            builders[builder.FunctionName] = builder;

            //var result = {maxDepth:0};
            //visitDepth(node,0,result);
            var maxDepth = 0;
            traverseWithParents(node, function (child) {
                // End of a path, save maxDepth if bigger.
                if (childrenLength(child) == 0) {
                    var depth = decisionAncestors(child, node).length;
                    if (maxDepth < depth) {
                        maxDepth = depth;
                    }
                }
            });
            builder.MaxNestingDepth = maxDepth;
            // if( maxDepth != result.maxDepth )
            // {
            //     console.log(builder.FunctionName, maxDepth, result.maxDepth);
            // }

            var result = { maxCond: 0 };
            // getMaxConditions(node, 0, result);

            var maxConditions = 0;
            traverseWithParents(node, function (child) {
                if (isDecisionConditional(child)) {
                    //console.log('in some kind of decision ' + child.type + ' || alt? ' + child.alternate + ' || cons? ' + child.consequent);
                    var conditions = getMaxConditions(child);
                    if (maxConditions < conditions) {
                        maxConditions = conditions;
                    }
                }
            });
            builder.MaxConditions = maxConditions;
        } else if (node.type === 'ImportDeclaration') {
            imports += 1;
        } else if (node.type === 'Identifier') {
            identifiers += 1;
        } else if (node.type === 'Literal') {
            literals += 1;
        } else if (node.type === 'VariableDeclaration') {
            vars += 1;
        } else if (isDecision(node)) {
            decisions++;
        }
    });
}

// Helper function for counting children of node.
function childrenLength(node) {
    var key, child;
    var count = 0;
    for (key in node) {
        if (node.hasOwnProperty(key)) {
            child = node[key];
            if (typeof child === 'object' && child !== null && key != 'parent') {
                count++;
            }
        }
    }
    return count;
}

// Helper function for checking if a node is a "decision type node"
function isDecision(node) {
    if (node.type == 'IfStatement') {
        // Don't double count else/else if
        if (node.parent && node.parent.type == 'IfStatement' && node.parent["alternate"]) {
            return false;
        }
        return true;
    }

    if (node.type == 'ForStatement' || node.type == 'WhileStatement' ||
        node.type == 'ForInStatement' || node.type == 'DoWhileStatement') {
        return true;
}
return false;
}

// Helper function for checking if a node is a "decision type node"
// Does not ignore else ifs so it can count the max conditions of a decision statement
function isDecisionConditional(node) {
    if (node.type == 'IfStatement' || node.type == 'ForStatement' || node.type == 'WhileStatement' ||
        node.type == 'ForInStatement' || node.type == 'DoWhileStatement') {
        return true;
}
return false;
}

// Helper function for printing out function name.
function functionName(node) {
    if (node.id) {
        return node.id.name;
    }
    return "anon function @" + node.loc.start.line;
}

// Helper function for printing out parameter count.
function getParameters(node) {
    var paramCount = 0;
    if (node.params != null) {
        paramCount = node.params.length;
        // don't need to loop through for just count
        // for (var i in node.params) { 
        //     // console.log('param: ' + node.params[i].name);
        //     paramCount++;
        // }
    } // else {no params}

    return paramCount;
}

// depth of decision
function decisionAncestors(node, scope) {
    var p = node.parent;
    var ancestors = [];
    while (p != null && p != scope) {
        if (isDecision(p))
            ancestors.push(p);
        p = p.parent;
    }
    return ancestors;
}

function visitDepth(node, depth, result) {
    var key, child;
    var children = 0;
    for (key in node) {
        if (node.hasOwnProperty(key)) {
            child = node[key];
            if (typeof child === 'object' && child !== null && key != 'parent') {
                children++;
                // Don't double count else/else if
                if (key == "alternate") {
                    visitDepth(child, depth, result)
                } else if (isDecision(child)) {
                    visitDepth(child, depth + 1, result);
                } else {
                    visitDepth(child, depth, result);
                }
            }
        }
    }

    if (children == 0) {
        if (result.maxDepth < depth) {
            result.maxDepth = depth;
        }
    }
}

// Helper function for getting Cyclomatic Complexity
function getCyclomaticComplexity(node) {
    var complexityCount = 0;
    traverseWithParents(node, function (n) {
        if (isDecision(n)) {
            complexityCount++;
        }
    });
    return complexityCount;
}

// Helper function to get max conditions 
function getMaxConditions(node) {
    var condiCount = 1;
    var maxCondiCount = 1; // decisions require 1 conditional at least
    traverseWithParents(node, function (n) {
        // if (node.consequent) {console.log('CONSEQUENT');} if (node.alternate) {console.log('ALT');}

        // HOWTO count conditionals, probably overly complicated...
        // 1st count entry into a decision and then add each logical expression after it,
        // if a new decision is reached then reset counter to 1 and start chain again.
        if (isDecisionConditional(n)) {
            // console.log('CUR COUNT: ' + condiCount + ' CUR MAX: ' + maxCondiCount);
            if (maxCondiCount < condiCount) {
                maxCondiCount = condiCount;
                // console.log('NEW MAX: ' + maxCondiCount);
            }
            condiCount = 1;
            //console.log('whatdo');
        }
        if (n.type == 'LogicalExpression') {
            condiCount++;
            //console.log('dowhat');
        }
    });

    if (maxCondiCount < condiCount) {
        maxCondiCount = condiCount;
        // console.log('NEW MAX: ' + maxCondiCount);
    }
    return maxCondiCount;
}

// Helper function for allowing parameterized formatting of strings.
if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
        });
    };
}

main();
