/** This script does nothing, except printing a small message to the console.
*   The console is a part of the browser where you can find feedback on how your scripts are doing
*   You can find it when you choose ‘inspect element’ and choose the ‘console’ tab
*/

console.log("started loading the thesis javascript");

/** 
Here we try to use the jQuery function $.find()
If jQuery is not properly defined (linked in from the HTML)
the console will show an error like:

Uncaught ReferenceError: $ is not defined

or

Uncaught TypeError: $.find is not a function(…)
*
*/
var $paragraphs = $.find("p");

if ($paragraphs) {
    console.log('found ' + $paragraphs.length + ' paragraphs in thesis');
}
