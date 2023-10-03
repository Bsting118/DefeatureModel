# Defeature Repo. Version Control Changelog
----------
### See below to find revisions on each main file in this repository.
<br>

<details>
<summary>Defeature Kits</summary>
<br>
<ul>
<li>Kit (V1)</li>
    <ul>
    <li>Summary: initial commit and the first defeature app.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>This is the first defeature app so all the code and files are new!</li>
        </ul>
    </details>
<li>KitV2</li>
    <ul>
    <li>Summary: changeover to force I/O string-processing to be in lowercase for consistent handling.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>All input variables, arrays, or any other means of input storage in the defeature Python program that reference the inputted defeature file or file lines now use the Python method <code>.lower()</code>.</li>
        </ul>
    </details>
<li>KitV3</li>
    <ul>
    <li>Summary: changeover to automatic GUI asset assembly of defeature app's interface.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Commented out and swapped programmatically-setup GUI code for a simple algorithm that tries to find the defeature GUI folder to use for assembling the user-interface of the app (banner images, icons, etc.). Reason for this is that the user shouldn't have to go and edit Python code before using the defeature app; too tedious.</li>
        <li>Refined past code comments.</li>
        </ul>
    </details>
<li>KitV3.2</li>
    <ul>
    <li>Summary: begun upgrading functions to filter I/O.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Upgraded <code>getRealValue()</code> Python function to pull its output from source, non-lowercased file lines.</li>
        <li>Added whitespace removal filter to <code>getRealValue()</code> right before it returns for more accurate output.</li>
        </ul>
    </details>
<li>KitV3.3</li>
    <ul>
    <li>Summary: updated RBSpringPreload and RBSpringStiffness mutators/accessors.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Replaced code of both <code>changeRBSpringPreloadToVal()</code> and <code>changeRBSpringStiffToVal()</code> with instead real value functions for changing the spring coefficients; now using <code>getRealValue()</code> for code consistency.</li>
        <li>Both <code>getRBSpringPreload()</code> and <code>getRBSpringStiffness()</code> Python functions have been updated to use ping-pong index functions (e.g., <code>findStartOfBlock+1</code>) for checking that the correct header keyword is present during file processing.</li>
        </ul>
    </details>
<li>KitV3.4</li>
    <ul>
    <li>Summary: filtered I/O processing + function updates.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Updated <code>getCFactor()</code>, <code>getPressAngle()</code>, and <code>getHelixAngle()</code> to use ping-pong algorithm references instead of previous line indices.</li>
        <li>For file output, pulls from source file's lines instead of post-processed lowercase input to prevent bad output.</li>
        </ul>
    </details>
<li>KitV3.5</li>
    <ul>
    <li>Summary: string data changeover.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Accessors now return string real-values instead of Python-floats in order to prevent decimal cutoffs; they are the following:</li>
            <ul>
            <li><code>getRBSpringPreload()</code></li>
            <li><code>getRBSpringStiffness()</code></li>
            <li><code>getHelixAngle()</code></li>
            <li><code>getPressAngle()</code></li>
            <li><code>getCFactor()</code></li>
            <li><code>getNewRPGearSepEqu()</code></li>
            </ul>
        </ul>
    </details>
<li>KitV3.6</li>
    <ul>
    <li>Summary: latest stable and updated version of defeature model Python app.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Fixed progress bar to no longer lag statuses.</li>
        <li>Defeature functions, <code>findAndRemoveUnassociated()</code> and <code>findAndReplaceAssociated()</code>, have been programmed to use the ping-pong algorithm instead of OBS prev-line lookup context (note: lowered performance by a few seconds but upgraded robustness).</li>
        </ul>
    </details>
</ul>
</details>

<details>
<summary>Defeature Source Code</summary>
<br>
<ul>
<li>Source Code</li>
    <ul>
    <li>Summary: backed up the source code of the first defeature model kit.</li>
    </ul>
<li>Upgraded Source Code V2</li>
    <ul>
    <li>Summary: uploaded source code file from V2 kit per revision.</li>
    </ul>
<li>Upgraded Source Code V3</li>
    <ul>
    <li>Summary: uploaded all source code files from V3 kits per each revision.</li>
    </ul>
</ul>
</details>

<details>
<summary>Defeature Documentation</summary>
<br>
<ul>
<li>Dictionary</li>
    <ul>
    <li>Summary: the manual documentation for showing what each function does in the defeature program, updated to also list corresponding return types for API purposes.</li>
    </ul>
    <details>
    <summary>Changes:</summary>
        <ul>
        <li>Added return type descriptions to each function's documentation.</li>
        </ul>
    </details>
<li>Read Me</li>
    <ul>
    <li>Summary: created as an overview of how to use this repository and the defeature program inside it.</li>
    </ul>
<li>Troubleshooting</li>
    <ul>
    <li>Summary: created as a common FAQ help document for using the defeature app.</li>
    </ul>
<li>How To Install Python</li>
    <ul>
    <li>Summary: created as a brief tutorial for new Python developers as to how to install the compatible Python version on their PC.</li>
    </ul>
<li>PyInstaller Training for Defeature Kits</li>
    <ul>
    <li>Summary: created to show Python developers how to install and work with the PyInstaller tool (for making kits/Python apps).</li>
    </ul>
<li>Python Code Basic Training</li>
    <ul>
    <li>Summary: created as an educative resource for users who would like to begin developing with Python or this defeature program.</li>
    </ul>
</ul>
</details>
