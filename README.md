# *Developer Manual - JUST Virtual Judge!*
This is a virtual which can help  to arrange contest where problems are collected from different sources. So far, user can create contest, particapate in different contests, see rank list among other features. They can also archive problems to use those for later contest. 

## How to run on local machine
- Download the project as zip or clone it.
- Go to root directory, run `pip install -r requirements.txt`.
- Activate the virtual environment.
- Go to root folder, run `python manage.py runserver`.

## How to contribute
- Check for impending issues. 
- If there isn't any and you want to implement any feature, then create a branch. 
- Implement your feature.
- Push it to the repo and make a pull request.


## *Apps*
Below the description for each app and the function used in them is given. 

## accounts
This app handles everything about related to user account. 
**registerPage:** 
- *Input:* 
`username, email, password, password confirmation` as form in Django

- *Method:*
Checks if the input form is valid.
`If valid` then saves the data and creates user.
`If not valid` Shows specific output for any failure.

- *Output:*
`On Success` redirects to login page.
`On Failure` Shows message "User was created for this username" if user name already exists. If password does not match, shoes message "Password did not match". If password is not strong then it show password criteria to make strong password.

**updateprofilepicture:**
 - *Input:* 
`image` 

- *Method:*
Checking profile of current user.
`If valid` then updates profile picture.
`If not valid` Shows specific output for any failure.

- *Output:*
`On Success` redirects to profile page.
`On Failure` shows <span style="color:red">*404*</span> error for invalid user.

**loginPage**
 - *Input:* 
`username,password` .

- *Method:*
`If valid` the user gets to login.
`If not valid` shows specific output for failures.

- *Output:*
`On Success` redirect to home page
`On Failure` show message "username or password is incorrect".

**logoutuser**
 - *Input:* 
`No input` 

- *Method:*
user requests to log out.
user logs out. 
- *Output:*
`On Success` render login page

**Home**
 - *Input:* 
`null` 
- *Method:*
gets username from user

- *Output:*
`On Success` renders home page

**profile**
 - *Input:* 
`null`.
- *Method:*
Sets ac, wa, th to 0 
`ac == accepted result, wa == wrong answer, th == any other result`
checks for status in submission using a loop
`if status == accpeted`, increments ac
`else if status == Wrong Answer`, increments wa
`else` increments th

- *Output:*
`On Success` renders profile
`On Failure` redirects to login page

**mysubmission**
 - *Input:* 
`null`.
- *Method:*
queries for all the submission.
using loop, it finds out problem title from each submission. 
[zips](https://www.w3schools.com/python/ref_func_zip.asp) submission and problems together.

- *Output:*
`On Success` renders mysubmission page.
`On Failure` redirects login page


## problems
This app handles adding, viewing and storing problems.
**addproblem**
 - *Input:* 
`ptitle,ptimelimit,pmemorylimit,pdescription,pinput,poutput,pexinput,pexoutput,psinput,psoutput,ptags,ptype,pnote,pshow`.
- *Method:*
saves problem to database. 

- *Output:*
`On Success` redirects to allproblems page.
`On Failure` redirects to login.

**viewproblems**
 - *Input:* 
`null`.
- *Method:*
Makes query for all problems.
- *Output:*
`On Success` redirects to allproblems page.

**problems**
 - *Input:* 
`lan, code`.
- *Method:*
gets keyword argument with request.
define support languages.
makes query for particular problems from pk 
removes markup tags using re.compile
creates a new submission
choose language and version from lan
then call post-api with parameters [clientId, clientSecret, script, stdin, language, versionIndex]
convert result into JSON file
`if` successCode is 200 `then`, re.compile the output and check time limit and memory limit
shows verdict
saves the result in database 

- *Output:*
`On Success` redirects to profile page.

## contests
**createcontestpage**
 - *Input:* 
`title, description, beginning date, beginning time, length, password`.

- *Method:*
`if` verdicts(beginning time, beginning date, length) passes, `then` create a new contest.
`else if` length is not equal 3, `then` show specific message for specific failure.
- *Output:*
`On Success` redirects to setproblem page.
`On failure` shows "Correct Your Formate like hour:min:sec" or "Hour Should be lessthan 100, min and sec Should be lessthan 60" or "Time Can't be negative" depending on failure type.
****

**setproblem**
 - *Input:* 
`problemlist`.
- *Method:*
Make query to get all the problems
`if` number of problems is outside the range of 1 to 10, `then` show message
`else` convert list into string, `then` set the contest problems
- *Output:*
`On Success` redirects to contest page.
`On Failure` Show message "You Must add 1 to 10 Problem". 

**contestpage**
 - *Input:* 
`null`
- *Method:*
Make query to get all the contests.
Divide them in to upcoming, running, ended depending starting and ending time. [datetime](https://www.w3schools.com/python/python_datetime.asp),  [strftime](https://www.programiz.com/python-programming/datetime/strftime), [timedelta](https://www.geeksforgeeks.org/python-datetime-timedelta-function/) has been used to divide contests according to date and time.

- *Output:*
`On Success` renders contest page.

**contesttask**
 - *Input:* 
`null`.
- *Method:*
Query specific contest from database.
Contest time is separated into date, month, year, hour, minute, second to check if the contest should be accessible. 
Check contest password.
`if` password matches, `and` contest started or finished, `then` user may enter the contest. 
`if` password matches, `and` contest has not started yet, `then` show "contest not started yet". 

- *Output:*
`On Success` redirects to task page.
`On Failure` redirects to login page.

**tasks**
 - *Input:* 
`null`.
- *Method:*
Query for specific contest.
Split the problems `and` put them in a list names props.
Show problems from the list.

- *Output:*
`On Success` renders to task page.
`On Failure` redirects to login page.

**contestpage**
 - *Input:* 
`code,lan`.

- *Method:*
Query for problem details.
Query for contest details.
Separate ending time into date, month, year, hour, minute, second to check if the contest ended.
Gets keyword argument with request.
Define support languages.
Makes query for particular problems from pk2. 
Separate current time into date, month, year, hour, minute, second to compare with ending time.
Check if the user has participated.
 Choose language and version from lan.
Removes markup tags using re.compile for code, input and output.
Creates a new submission and calculates current point for wrong answer/TLE/MLE. 
Then call post-api with parameters [clientId, clientSecret, script, stdin, language, versionIndex].
Convert result into JSON file.
`if` successCode is 200 `then`, re.compile the output and check time limit and memory limit.
If the problem was solved before, show a warning message.
For every TLE, MLE and wrong answer, extra penalty point will be added. 
Shows verdict.
Saves the result in database.

- *Output:*
`On Success` renders to task page.
`On Failure` redirects to login page.

**submissions**
 - *Input:* 
`null`.

- *Method:*
Query for submitted problems on this specific contest and specific user. 

- *Output:*
`On Success` renders submission page.
`On Failure` redirects to login page.

**viewsubmittedcode**
 - *Input:* 
`null`.

- *Method:*
Make query for code of specific problem that has been submitted.

- *Output:*
`On Success` renders to viewsubmittedcode page.
`On Failure` redirects to login page.

**Ranklist**
 - *Input:* 
`null`.
- *Method:*
Query for participants in a specific contest
Sort participants according to points
Show the list

- *Output:*
`On Success` renders to ranklist page.
`On Failure` redirects to login page.

