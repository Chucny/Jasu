

<body>

<h1>Jasu Language 🟢</h1>
<p><strong>Jasu</strong> is a lightweight, Python-based interpreted language designed for fun scripting with simple and intuitive syntax.</p>

<h2>Syntaxes</h2>
<ul>
    <li>Variables with <code>var</code></li>
    <li>Functions with <code>define[...]</code></li>
    <li>Conditional branching: <code>if</code>, <code>elif</code>, <code>else</code></li>
    <li>Loops: <code>while(){}</code></li>
    <li>Input/Output: <code>read()</code> and <code>write()</code></li>
    <li>Wait / Sleep: <code>wait(seconds)</code></li>
    <li>String manipulation: <code>.replace(old, new)</code> and slicing <code>[start:end]</code></li>
    <li>HTTP requests: <code>fetch(url, method)</code></li>
    <li>Control flow: <code>#return()</code> and <code>#break()</code></li>
</ul>

<h2>Syntax Reference</h2>

<h3>Variables</h3>
<pre><code>var name = "Alice";
var age = 25;
var result = greet(name);
</code></pre>
<p>Variables can store anything, including the result of a function call.</p>

<h3>Functions</h3>
<pre><code>define[greet(person)]{
    write("Hello " + person);
    #return("Done");
}

var response = greet("Alice");
write(response);
</code></pre>

<h3>Conditional Statements</h3>
<pre><code>if(name == "Alice"){
    write("Hello Alice");
}
elif(name == "Bob"){
    write("Hi Bob");
}
else{
    write("Hello stranger");
}
</code></pre>

<h3>Loops</h3>
<pre><code>var count = 0;
while(count < 5){
    write(count);
    count = count + 1;
    if(count == 3){
        #break();
    }
}
</code></pre>

<h3>Input / Output</h3>
<pre><code>var username = read("Enter your name: ");
write("Hello " + username, color=green);
</code></pre>

<h3>Wait / Sleep</h3>
<pre><code>wait(2);  // waits for 2 seconds
</code></pre>

<h3>String Manipulation</h3>
<pre><code>var text = "Hello world";
text = text.replace("world", "Jasu");
write(text[0:5]); // prints "Hello"
</code></pre>

<h3>HTTP Fetch</h3>
<pre><code>var html = fetch("https://www.google.com");
write(html[0:100]);
</code></pre>

<h3>Control Flow</h3>
<pre><code>#return("value");  // returns from a function
#break();             // breaks a loop
</code></pre>

<h2>Write with Color</h2>
<pre><code>write("Hello", color=red);
write("World", color=green);
</code></pre>

<p>Jasu allows embedding any function call inside a variable, supports zero-based indexing, and lets you define dynamic functions using <code>define[...]</code>. The compiler syntax is: <code>run_jasu(""" code """)</code></p>
<br><strong>Copyright &copy; Chucny 2026</strong>

</body>
</html>
