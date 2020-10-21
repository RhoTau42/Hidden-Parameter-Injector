# Hidden-Parameter-Injector
inject.py, Tries to inject hidden common parameters to basic HTTP requests. Reveals any hidden parameters if any were accepted and changed the content of the page.

## Usage:
* make sure you the latest upgrade of urlib3: `python3 -m pip install --upgrade urllib3`
1. `python3 inject.py -u http://localhost/`
2. If you want to use a urls list and run with all of them you can by using `--urls` followed by an urls list.
3. Change the parameters wordlists with `-f` followed by the file you want the script to read from.
4. See results in `accepted_params.json`

## Script Work Flow:
1. Parsing the URLs file and parameters wordlist.
2. Getting the original content length of the webpage.
3. Itereates through the parameters, requesting the page with the parameters.
4. If any parameters were accepted - adds them to the list of accepted parameteres.
5. Finally saves results to `accpeted_params.json`
    * If you want, change that with `-o` followed by the output file name (No need to provide file extenstion as the script adds ".json" to the end if the file doens't end with ".json" extension
