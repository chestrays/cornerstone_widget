// Simple IPython Notebook test
// Requires PhantomJS and CasperJS.
// To run:
// 1) Start a notebook server in an empty directory.
// 2) casperjs test_basic.js

var casper = require('casper').create({
    // verbose: true,
    // logLevel: "debug"
});

casper.start('http://127.0.0.1:8765',function () {
});

casper.thenOpen('http://127.0.0.1:8765/new');

casper.then(function () {
   this.echo(this.getCurrentUrl());  
});

casper.then(function () {
    this.evaluate(function () {
        var cell = IPython.notebook.get_selected_cell();
        cell.set_text('a=10; print a');
        cell.execute();
    });
});

casper.wait(2000);

casper.then(function () {
    var result = this.evaluate(function () {
        // This code is run in the pages context.
        // All of our custom JavaScript objects can be used.
        IPython.notebook.save_notebook();
        var cell = IPython.notebook.get_cell(0);
        // And jQuery works too!
        var output = cell.element.find('.output_area').find('pre').html();
        return output        
    })
    // Tests can be written in a familiar form
    this.test.assertEquals(result, '10\n', 'stdout output matches')
});

casper.back();

casper.thenEvaluate(function () {
    // Click the Shutdown button.
    $('#project_name').next().find('button').click();
})

casper.wait(1000);

casper.thenEvaluate(function () {
    // Click the Delete button and confirm.
    $('#project_name').next().find('button').click();
    $('.ui-dialog').find('button').first().click();
})

casper.wait(1000);

casper.run(function () {
    this.test.renderResults(true);
});
