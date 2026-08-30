import json
import os

sandbox_data = {
    'python': [
        {'title': 'Reverse String', 'desc': 'Write a function reverse_string(s) that returns the reversed string.', 'lang': 'python', 'code': 'def reverse_string(s):\n    # Write your code here\n    pass\n'},
        {'title': 'Flatten List', 'desc': 'Write a function flatten(lst) that flattens a nested 2D list into a 1D list.', 'lang': 'python', 'code': 'def flatten(lst):\n    pass\n'},
        {'title': 'Dictionary Merge', 'desc': 'Write a function merge_dicts(d1, d2) that merges two dictionaries. d2 values should overwrite d1.', 'lang': 'python', 'code': 'def merge_dicts(d1, d2):\n    pass\n'},
        {'title': 'Find Duplicates', 'desc': 'Write a function find_dups(lst) returning a list of items that appear more than once.', 'lang': 'python', 'code': 'def find_dups(lst):\n    pass\n'},
        {'title': 'Simple OOP', 'desc': 'Create a class User with an __init__ taking name and a method get_name().', 'lang': 'python', 'code': 'class User:\n    pass\n'}
    ],
    'javascript': [
        {'title': 'Filter Evens', 'desc': 'Write a function filterEvens(arr) returning only even numbers from the array.', 'lang': 'javascript', 'code': 'function filterEvens(arr) {\n    // Write your code here\n}'},
        {'title': 'Promise Timeout', 'desc': 'Write a function delay(ms) that returns a Promise resolving after ms milliseconds.', 'lang': 'javascript', 'code': 'function delay(ms) {\n\n}'},
        {'title': 'Deep Clone', 'desc': 'Write a function deepClone(obj) to perform a basic deep clone of a JSON-serializable object.', 'lang': 'javascript', 'code': 'function deepClone(obj) {\n\n}'},
        {'title': 'Debounce', 'desc': 'Implement a basic debounce(fn, delay) function.', 'lang': 'javascript', 'code': 'function debounce(fn, delay) {\n\n}'},
        {'title': 'Array Reduce', 'desc': 'Use reduce to write sumArray(arr) that sums all numbers in an array.', 'lang': 'javascript', 'code': 'function sumArray(arr) {\n\n}'}
    ],
    'react': [
        {'title': 'Counter Component', 'desc': 'Create a React component <Counter /> with a button that increments a displayed count.', 'lang': 'javascript', 'code': 'import React, { useState } from "react";\n\nexport default function Counter() {\n  return <div></div>;\n}'},
        {'title': 'Fetch Data useEffect', 'desc': 'Write a component <DataList /> that fetches from /api/data on mount and maps the result to <li>.', 'lang': 'javascript', 'code': 'import React, { useState, useEffect } from "react";\n\nexport default function DataList() {\n  return <ul></ul>;\n}'},
        {'title': 'Toggle Visibility', 'desc': 'Create a <Toggle /> component that shows/hides a <p>Hello</p> when a button is clicked.', 'lang': 'javascript', 'code': 'import React, { useState } from "react";\n\nexport default function Toggle() {\n  return <div></div>;\n}'},
        {'title': 'Controlled Input', 'desc': 'Create a controlled <input> inside a <Form /> component that alerts the value on submit.', 'lang': 'javascript', 'code': 'import React, { useState } from "react";\n\nexport default function Form() {\n  return <form></form>;\n}'},
        {'title': 'Context Consumer', 'desc': 'Consume a ThemeContext and apply the theme string as a className to a div.', 'lang': 'javascript', 'code': 'import React, { useContext } from "react";\nimport { ThemeContext } from "./theme";\n\nexport default function ThemedDiv() {\n  return <div></div>;\n}'}
    ],
    'node.js': [
        {'title': 'Basic HTTP Server', 'desc': 'Create an HTTP server listening on port 3000 that responds with "Hello World".', 'lang': 'javascript', 'code': 'const http = require("http");\n\n// Create server here\n'},
        {'title': 'Async File Read', 'desc': 'Write a function readConfig() that uses fs.promises.readFile to read "config.json".', 'lang': 'javascript', 'code': 'const fs = require("fs").promises;\n\nasync function readConfig() {\n\n}'},
        {'title': 'Express Route', 'desc': 'Write an Express GET route for /users/:id that returns the id as JSON.', 'lang': 'javascript', 'code': 'const express = require("express");\nconst app = express();\n\n// Add route here\n'},
        {'title': 'Event Emitter', 'desc': 'Create a custom Emitter class extending EventEmitter that emits "start" on a trigger method.', 'lang': 'javascript', 'code': 'const EventEmitter = require("events");\n\nclass Emitter extends EventEmitter {\n\n}'},
        {'title': 'Crypto Hash', 'desc': 'Use the crypto module to return a sha256 hash (hex) of a given string.', 'lang': 'javascript', 'code': 'const crypto = require("crypto");\n\nfunction hash(str) {\n\n}'}
    ],
    'sql': [
        {'title': 'Select Active Users', 'desc': 'Write a SQL query to select all users where status is "active".', 'lang': 'sql', 'code': '-- Write your SQL query here\nSELECT * FROM users;'},
        {'title': 'Join Tables', 'desc': 'Write a SQL query to JOIN users and orders on user_id.', 'lang': 'sql', 'code': '-- Write your SQL query here\n'},
        {'title': 'Count by Group', 'desc': 'Write a query to count the number of orders per user_id.', 'lang': 'sql', 'code': '-- Write your SQL query here\n'},
        {'title': 'Subquery', 'desc': 'Write a query to find users whose age is greater than the average age.', 'lang': 'sql', 'code': '-- Write your SQL query here\n'},
        {'title': 'Update Records', 'desc': 'Write a query to update the status to "inactive" for users last_login < 2023.', 'lang': 'sql', 'code': '-- Write your SQL query here\n'}
    ],
    'docker': [
        {'title': 'Basic Dockerfile', 'desc': 'Write a Dockerfile to use node:18, copy files, run npm install, and start index.js.', 'lang': 'dockerfile', 'code': 'FROM node:18\n\n# Add instructions here\n'},
        {'title': 'Expose Port', 'desc': 'Write a Dockerfile instruction to expose port 8080.', 'lang': 'dockerfile', 'code': '# Write your Dockerfile instruction here\n'},
        {'title': 'Volume Mount', 'desc': 'Write the docker run flag to mount local ./data to /app/data in the container.', 'lang': 'shell', 'code': '# Write your docker run command here\ndocker run -d image_name'},
        {'title': 'Docker Compose', 'desc': 'Write a basic docker-compose.yml with a web service and a db service (postgres).', 'lang': 'yaml', 'code': 'version: "3"\nservices:\n'},
        {'title': 'Multi-stage Build', 'desc': 'Write a multi-stage Dockerfile that builds in a golang image and copies to alpine.', 'lang': 'dockerfile', 'code': 'FROM golang:1.20 AS builder\n\nFROM alpine:latest\n'}
    ],
    'html': [
        {'title': 'Semantic Structure', 'desc': 'Write an HTML skeleton with header, nav, main, and footer tags.', 'lang': 'html', 'code': '<!DOCTYPE html>\n<html>\n<body>\n\n</body>\n</html>'},
        {'title': 'Form Inputs', 'desc': 'Create a form with a text input for username, password input, and a submit button.', 'lang': 'html', 'code': '<form>\n\n</form>'},
        {'title': 'Table with Headers', 'desc': 'Create an HTML table with Name and Age headers, and one row of data.', 'lang': 'html', 'code': '<table>\n\n</table>'},
        {'title': 'Accessible Image', 'desc': 'Write an img tag with proper alt text and wrap it in a figure with a figcaption.', 'lang': 'html', 'code': '<!-- Write your HTML here -->\n'},
        {'title': 'Video Embed', 'desc': 'Write a video tag with controls and a source pointing to "video.mp4".', 'lang': 'html', 'code': '<!-- Write your HTML here -->\n'}
    ],
    'css': [
        {'title': 'Flexbox Center', 'desc': 'Write CSS to perfectly center a child div horizontally and vertically using flexbox.', 'lang': 'css', 'code': '.container {\n  /* Add flexbox rules here */\n}'},
        {'title': 'CSS Grid', 'desc': 'Write CSS to create a 3-column grid layout with equal widths.', 'lang': 'css', 'code': '.grid-container {\n  /* Add grid rules here */\n}'},
        {'title': 'Hover Transition', 'desc': 'Add a transition rule to scale a button to 1.1 on hover smoothly over 0.3s.', 'lang': 'css', 'code': 'button {\n\n}\nbutton:hover {\n\n}'},
        {'title': 'Media Query', 'desc': 'Write a media query that changes the background color to blue on screens smaller than 600px.', 'lang': 'css', 'code': '/* Write media query here */\n'},
        {'title': 'CSS Variables', 'desc': 'Define a custom property --main-color: red on the :root and apply it to h1.', 'lang': 'css', 'code': ':root {\n\n}\nh1 {\n\n}'}
    ]
}

debugging_data = {
    'python': [
        {'title': 'Mutable Default Args', 'desc': 'Fix the bug where the default list argument retains state across calls.', 'lang': 'python', 'code': 'def add_item(item, lst=[]):\n    lst.append(item)\n    return lst'},
        {'title': 'UnboundLocalError', 'desc': 'Fix the bug where the local variable count is referenced before assignment.', 'lang': 'python', 'code': 'count = 0\ndef increment():\n    count += 1\n    return count'},
        {'title': 'KeyError', 'desc': 'Fix the bug so it returns None instead of throwing a KeyError if the key is missing.', 'lang': 'python', 'code': 'def get_user_age(user_dict):\n    return user_dict["age"]'}
    ],
    'javascript': [
        {'title': 'Lost 	his Context', 'desc': 'Fix the bug where 	his.name is undefined inside the setTimeout callback.', 'lang': 'javascript', 'code': 'const user = {\n  name: "Alice",\n  greet() {\n    setTimeout(function() {\n      console.log(this.name);\n    }, 1000);\n  }\n};'},
        {'title': 'Var in Loop', 'desc': 'Fix the loop so it logs 0, 1, 2 instead of 3, 3, 3.', 'lang': 'javascript', 'code': 'for (var i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 100);\n}'},
        {'title': 'Off by One', 'desc': 'Fix the loop bounds so it iterates over all elements without returning undefined.', 'lang': 'javascript', 'code': 'function logItems(arr) {\n  for (let i = 0; i <= arr.length; i++) {\n    console.log(arr[i]);\n  }\n}'}
    ],
    'react': [
        {'title': 'Direct State Mutation', 'desc': 'Fix the bug where state is mutated directly instead of using the setter.', 'lang': 'javascript', 'code': 'function Counter() {\n  const [count, setCount] = useState(0);\n  const inc = () => {\n    count = count + 1;\n    setCount(count);\n  };\n}'},
        {'title': 'Missing Dependency', 'desc': 'Fix the useEffect so it properly tracks the userId dependency.', 'lang': 'javascript', 'code': 'useEffect(() => {\n  fetchData(userId);\n}, []);'},
        {'title': 'Missing Key Prop', 'desc': 'Fix the map function to include a unique key for each list item.', 'lang': 'javascript', 'code': 'function List({ items }) {\n  return items.map(item => <li>{item.name}</li>);\n}'}
    ],
    'node.js': [
        {'title': 'Double Send', 'desc': 'Fix the Express route so it doesnt crash with "Cannot set headers after they are sent".', 'lang': 'javascript', 'code': 'app.get("/user", (req, res) => {\n  if (!req.query.id) res.send("No ID");\n  res.send("User ID: " + req.query.id);\n});'},
        {'title': 'Unhandled Promise', 'desc': 'Fix the async route to properly catch and pass errors to Express error handler.', 'lang': 'javascript', 'code': 'app.get("/data", async (req, res, next) => {\n  const data = await fetchFromDB();\n  res.json(data);\n});'},
        {'title': 'Callback Error Swallowed', 'desc': 'Fix the fs.readFile callback to properly handle the error parameter.', 'lang': 'javascript', 'code': 'fs.readFile("config.json", (err, data) => {\n  console.log(data.toString());\n});'}
    ],
    'sql': [
        {'title': 'NULL Equality Bug', 'desc': 'Fix the query to correctly select rows where deleted_at is NULL.', 'lang': 'sql', 'code': 'SELECT * FROM users WHERE deleted_at = NULL;'},
        {'title': 'Ambiguous Column', 'desc': 'Fix the JOIN query so the id column in the SELECT is not ambiguous.', 'lang': 'sql', 'code': 'SELECT id, name, order_date \nFROM users \nJOIN orders ON users.id = orders.user_id;'},
        {'title': 'Missing Group By', 'desc': 'Fix the aggregate query by adding the necessary GROUP BY clause.', 'lang': 'sql', 'code': 'SELECT department, COUNT(id) \nFROM employees;'}
    ],
    'docker': [
        {'title': 'Inefficient Cache', 'desc': 'Fix the Dockerfile order to cache npm install unless package.json changes.', 'lang': 'dockerfile', 'code': 'FROM node:18\nCOPY . .\nRUN npm install\nCMD ["node", "index.js"]'},
        {'title': 'Root User', 'desc': 'Add an instruction to run the container as a non-root user "node".', 'lang': 'dockerfile', 'code': 'FROM node:18\nCOPY . /app\nWORKDIR /app\nCMD ["node", "app.js"]'},
        {'title': 'Missing Expose', 'desc': 'Fix the Dockerfile by documenting that the app listens on port 8080.', 'lang': 'dockerfile', 'code': 'FROM nginx:alpine\nCOPY ./html /usr/share/nginx/html'}
    ],
    'html': [
        {'title': 'Unclosed Tag', 'desc': 'Fix the unclosed tag that is breaking the layout.', 'lang': 'html', 'code': '<div>\n  <p>Hello World\n</div>'},
        {'title': 'Duplicate IDs', 'desc': 'Fix the duplicate IDs, as IDs must be unique in an HTML document.', 'lang': 'html', 'code': '<button id="submit-btn">Save</button>\n<button id="submit-btn">Cancel</button>'},
        {'title': 'Form Action', 'desc': 'Fix the form so it submits via POST to /api/login.', 'lang': 'html', 'code': '<form>\n  <input name="user" />\n  <button type="submit">Login</button>\n</form>'}
    ],
    'css': [
        {'title': 'Specificity Issue', 'desc': 'Fix the CSS so the button class overrides the generic button tag color.', 'lang': 'css', 'code': 'button {\n  color: red !important;\n}\n.btn-primary {\n  color: blue;\n}'},
        {'title': 'Inline Dimensions', 'desc': 'Fix the display property so the span respects width and height.', 'lang': 'css', 'code': 'span {\n  display: inline;\n  width: 100px;\n  height: 100px;\n}'},
        {'title': 'Missing Unit', 'desc': 'Fix the margin property by adding the correct unit.', 'lang': 'css', 'code': '.box {\n  margin: 10 20;\n}'}
    ]
}

os.makedirs('app/data/sandbox', exist_ok=True)
os.makedirs('app/data/debugging', exist_ok=True)

for skill, items in sandbox_data.items():
    formatted_items = []
    for idx, item in enumerate(items):
        item['id'] = idx + 1
        item['skill'] = skill
        formatted_items.append(item)
    with open(f'app/data/sandbox/{skill}.json', 'w') as f:
        json.dump(formatted_items, f, indent=4)

for skill, items in debugging_data.items():
    formatted_items = []
    for idx, item in enumerate(items):
        item['id'] = idx + 1
        item['skill'] = skill
        formatted_items.append(item)
    with open(f'app/data/debugging/{skill}.json', 'w') as f:
        json.dump(formatted_items, f, indent=4)

