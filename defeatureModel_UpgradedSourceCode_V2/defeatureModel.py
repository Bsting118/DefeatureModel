#==================================
# defeatureModel.py (Source Code)
#==================================
# Nexteer Automotive 
# Programmed by: Brendan Sting
# Version 2
#==================================
# Date Uploaded: 5-4-2023
#==================================

#-----------------------------------------------------------------------------------------------------------------------
# List of Python Packages for use
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
import shutil
import threading
#-----------------------------------------------------------------------------------------------------------------------
# List of global Python variables:

defeatureFile = ""
defeatureFile = r"" + defeatureFile + ""
backupFile = ""

# Test this fileName with a print statement before using in equations
fullFileName = os.path.basename(defeatureFile) # File extension still attached; need to cut that off
extensionIndex = fullFileName.find(".")
fileName = fullFileName[0:extensionIndex]

# GUI Global Variables:
isOkButtonPressed = False
isBrowseButtonPressed = False
chosenFile = ""
#-----------------------------------------------------------------------------------------------------------------------
# This function finds the index of a keyword in a file
def findIndexOf(keyword, fileLines, lengthOfFile):
    indexOf = 0
    while indexOf < lengthOfFile:
        if keyword in fileLines[indexOf]:
            break
        indexOf = indexOf + 1

    return indexOf
#-----------------------------------------------------------------------------------------------------------------------
# Step one function of Removing Parameters documentation
def removeCylinder():
    # Keyword used in Ctrl+F and how program will find block top-down
    keyword = "cylinder"

    # Open the CMD file to edit as a TXT file to scan first
    length = fileLength(defeatureFile)
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    cylName = ""

    # Scan through the file
    for index, line in enumerate(file):
        line = line.lower()  # Improvement for String handling
        if keyword in line:
            # Remove the cylinder instance while also getting the actual cylinder's name for extra removal
            if "geometry create" in line:
                cylName = getCylinderName(index)
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, lines)

            # Extra removal: if cylinder instance still exists in attr., remove that block where it is as well
            if hasKeyword(cylName, lines):
                indexOfCyl = findIndexOf(cylName, lines, length)
                newEndOfBlock = findEndOfBlock(indexOfCyl)
                newStartOfBlock = findStartOfBlock(newEndOfBlock)
                if "geometry attributes" in lines[newStartOfBlock + 1]:
                    removeBlock(newStartOfBlock, lines)

            break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Finds the end (index) of the block of text using inputted starting line index
def findEndOfBlock(startLineIndex):
    # The symbol to go to after the starting line index in the TXT file
    delimiter = "!"

    # The default or initial value of the ending line index number
    endLineIndex = 0

    file = open(defeatureFile, "r")

    # Loop through file and start checking for "!" after the starting line index is reached
    for index, line in enumerate(file):
        if index > startLineIndex:  # bug was here with "!" being sense at same index as start
            if delimiter in line:
                endLineIndex = index
                break  # Added to for bugfix

    file.close()
    return endLineIndex
#-----------------------------------------------------------------------------------------------------------------------
# Finds the starting "!" delimiter as the start point of a block using the end point of the block as ref.
def findStartOfBlock(endLineIndex):
    # The delimiter indicating, in this instance, the top of the block or start of the block
    delimiter = "!"

    # Initialize start line index so that it can be updated later
    startLineIndex = 0

    # Open de-feature file to read from to find the desired start line index
    lines = open(defeatureFile, "r").readlines()

    # While-loop that will start from the passed end line index and go backwards/up in file until it finds start ("!")
    while endLineIndex > 0:
        # Decrement first so it doesn't sense delimiter right at the same end point
        endLineIndex = endLineIndex - 1
        if delimiter in lines[endLineIndex]:
            startLineIndex = endLineIndex
            break

    return startLineIndex
#-----------------------------------------------------------------------------------------------------------------------
# Removes a block of text in a TXT file using a starting point and the file's contents as input
def removeBlock(blockStart, fileLines):
    blockEnd = findEndOfBlock(blockStart)
    del(fileLines[blockStart:blockEnd])
    updatedFile = open(defeatureFile, "w+").writelines(fileLines)
    # Changed above variable to updatedFile which will instead of writing to a new one, will override previous
#-----------------------------------------------------------------------------------------------------------------------
# Removes a entire segment containing varying amounts of blocks by specifying the file and start and end of the removal
def removeSegment(segmentStart, segmentEnd, fileLines):
    del(fileLines[segmentStart:segmentEnd])
    updatedFile = open(defeatureFile, "w+").writelines(fileLines)
#-----------------------------------------------------------------------------------------------------------------------
# Finds a keyword and returns true or false based on if it found it or not
def hasKeyword(keyword, fileLines):
    found = False
    for line in fileLines:
        if keyword in line:
            found = True
            break
    return found
#-----------------------------------------------------------------------------------------------------------------------
# Removes a cylinder reference top-down order from file
def removeCylinderRef():
    # Keyword used in Ctrl+F and how program will find block top-down (changed from cylRef to cylref for handling)
    keyword = "cylref"

    # Open the CMD file to edit as a TXT file to scan first
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()

    # Scan through the file until we find the cylinder ref. instance
    for index, line in enumerate(file):
        line = line.lower()  # Improvement with String handling
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, lines)
            break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Removes a marker modify top-down order from file
def removeMarkerModify():
    # Keyword used in Ctrl+F and how program will find block top-down
    keyword = "marker modify"

    # Open the CMD file to edit as a TXT file to scan first
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()

    # Scan through the file until we find the marker modify instance
    for index, line in enumerate(file):
        line = line.lower()  # Improvement for String handling
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, lines)
            break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Eliminating all cylinder creations with automatic updating and removal
def removeAllCylinders():
    currentFile = open(defeatureFile).readlines()
    # Added this for loop for String handling (reads lines in lower-case only)
    for index, line in enumerate(currentFile):
        currentFile[index] = currentFile[index].lower()
    while (hasKeyword("cylinder", currentFile)):
        removeCylinder()
        currentFile = open(defeatureFile).readlines()
        for ind, line in enumerate(currentFile):
            currentFile[ind] = currentFile[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# Eliminating all cylinder references in markers (except the joint ones that stay)
def removeAllCylinderRefs():
    currentFile = open(defeatureFile).readlines()
    # Added this for loop for String handling (reads lines in lower-case only)
    for index, line in enumerate(currentFile):
        currentFile[index] = currentFile[index].lower()
    while (hasKeyword("cylRef", currentFile)) or (hasKeyword("cylref", currentFile)):
        removeCylinderRef()
        currentFile = open(defeatureFile).readlines()
        for ind, line in enumerate(currentFile):
            currentFile[ind] = currentFile[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# Eliminating all marker modify blocks
def removeAllMarkerModifies():
    currentFile = open(defeatureFile).readlines()
    # Added this for loop for String handling (reads lines in lower-case only)
    for index, line in enumerate(currentFile):
        currentFile[index] = currentFile[index].lower()
    while (hasKeyword("marker modify", currentFile)):
        removeMarkerModify()
        currentFile = open(defeatureFile).readlines()
        for ind, line in enumerate(currentFile):
            currentFile[ind] = currentFile[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# Gets the CFactor real value
def getCFactor():
    # Local variables to be referenced both inside and outside of loops:
    keyword = "rpCFactor"
    # Added for String handling (lower-case only)
    keyword = keyword.lower()
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    cFactorVal = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value for CFactor is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            prevLine = lines[lineNumber - 1]
            prevLine = prevLine.lower()
            if headerKeyword in prevLine:
                indexOfVal = index
                break

    # Use previously saved index of CFactor block and search for subsequent real_value line until end of CFactor block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValueString = realValueLine[snipStartIndex:snipEndIndex]
            realValueActual = float(realValueString)
            cFactorVal = realValueActual
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found CFactor value as a double
    return cFactorVal
#-----------------------------------------------------------------------------------------------------------------------
# Gets the pressure angle real value
def getPressAngle():
    # Local variables to be referenced both inside and outside of loops:
    keyword = "rpNormPressAng"
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    keyword = keyword.lower()
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    pressAngleVal = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value for Press. Angle is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            prevLine = lines[lineNumber - 1]
            prevLine = prevLine.lower()
            if headerKeyword in prevLine:
                indexOfVal = index
                break

    # Use previously saved index of PressAng block and search for subsequent real_value line until end of PressAng block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValueString = realValueLine[snipStartIndex:snipEndIndex]
            realValueActual = float(realValueString)
            pressAngleVal = realValueActual
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found Pressure Angle value as a double
    return pressAngleVal
#-----------------------------------------------------------------------------------------------------------------------
# Gets the helix angle real value
def getHelixAngle():
    # Local variables to be referenced both inside and outside of loops:
    keyword = "rackHelixAng"
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    keyword = keyword.lower()
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    helixAngleVal = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value for CFactor is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            prevLine = lines[lineNumber - 1]
            prevLine = prevLine.lower()
            if headerKeyword in prevLine:
                indexOfVal = index
                break

    # Use previously saved index of CFactor block and search for subsequent real_value line until end of CFactor block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValueString = realValueLine[snipStartIndex:snipEndIndex]
            realValueActual = float(realValueString)
            helixAngleVal = realValueActual
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found CFactor value as a double
    return helixAngleVal
#-----------------------------------------------------------------------------------------------------------------------
# Gets the rack brg spring stiffness real value
def getRBSpringStiffness():
    # Local variables to be referenced both inside and outside of loops:
    keyword = "rackBrgSpr_stiff"
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    keyword = keyword.lower()
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    RBSpringStiffVal = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            prevLine = lines[lineNumber - 1]
            prevLine = prevLine.lower()
            if headerKeyword in prevLine:
                indexOfVal = index
                break

    # Use previously saved index of block and search for subsequent real_value line until end of block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValueString = realValueLine[snipStartIndex:snipEndIndex]
            realValueActual = float(realValueString)
            RBSpringStiffVal = realValueActual
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found spring stiffness value as a double
    return RBSpringStiffVal
#-----------------------------------------------------------------------------------------------------------------------
# Gets the rack brg spring preload real value
def getRBSpringPreload():
    # Local variables to be referenced both inside and outside of loops:
    keyword = "rackBrgSpr_preload"
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    keyword = keyword.lower()
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    RBSpringPreloadVal = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            prevLine = lines[lineNumber - 1]
            prevLine = prevLine.lower()
            if headerKeyword in prevLine:
                indexOfVal = index
                break

    # Use previously saved index of block and search for subsequent real_value line until end of block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValueString = realValueLine[snipStartIndex:snipEndIndex]
            realValueActual = float(realValueString)
            RBSpringPreloadVal = realValueActual
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found spring preload value as a double
    return RBSpringPreloadVal
#-----------------------------------------------------------------------------------------------------------------------
# General function of getting a real value from a keyword/variable (this should be used more)
def getRealValue(keyword):
    # Local variables to be referenced both inside and outside of loops:
    headerKeyword = "variable create"
    valueKeyword = "real_value"
    headerKeyword = headerKeyword.lower()
    valueKeyword = valueKeyword.lower()
    keyword = keyword.lower()
    indexOfVal = 0
    endOfBlock = 0
    realValue = 0

    # Open the file and content for scanning
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    for ind, line in enumerate(lines):
        lines[ind] = lines[ind].lower()

    # Loop through by index to find the exact block where the real_value is located; save a ref. index
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            if headerKeyword in lines[startOfBlock + 1]:
                indexOfVal = index
                break

    # Use previously saved index of block and search for subsequent real_value line until end of block
    while indexOfVal < endOfBlock:
        if valueKeyword in lines[indexOfVal]:
            realValueLine = lines[indexOfVal]
            snipStartIndex = (realValueLine.find("=") + 1)
            snipEndIndex = realValueLine.find("&")
            realValue = realValueLine[snipStartIndex:snipEndIndex]
            break
        indexOfVal = indexOfVal + 1

    file.close()

    # Return the found real value as a string (can be a single value or an array value)
    return realValue
#-----------------------------------------------------------------------------------------------------------------------
# This function gets the cylinder name inside a geometry block
def getCylinderName(indexOfGeometryBlock):
    # Initialize
    fileLines = open(defeatureFile).readlines()
    cylinderName = ""
    endOfFile = fileLength(defeatureFile)

    i = indexOfGeometryBlock
    while i < endOfFile:
        if "cylinder_name" in fileLines[i]:
            # If we found the cylinder name line, extract it
            snipStartIndex = fileLines[i].find("=") + 1
            snipEndIndex = fileLines[i].find("&")
            cylinderName = fileLines[i]
            cylinderName = cylinderName[snipStartIndex:snipEndIndex]
            break
        i = i + 1

    return cylinderName
#-----------------------------------------------------------------------------------------------------------------------
# General function for getting the full variable name of a variable keyword
def getFullVarName(keyword):
    # Initialize both file reading and the full variable name
    file = open(defeatureFile, "r")
    fullVarName = ""

    # Search for the line with the variable's keyword name then snip a substring of the full name
    for line in file:
        if keyword in line:
            if "variable_name" in line:
                snipStartIndex = line.find("=") + 1
                snipEndIndex = line.find("&")
                fullVarName = line[snipStartIndex:snipEndIndex]
                break

    file.close()
    return fullVarName
#-----------------------------------------------------------------------------------------------------------------------
# General function for removing a variable create definition block in the file
def removeVarCreate(keyword):
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    # Improvement with String handling
    keyword = keyword.lower()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:  # Keyword will be the name of the variable whose create block you want deleted
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            # The header is always one below the start which is top "!" (changed to include var name check)
            if ("variable create" in lowerCaseLines[startOfBlock + 1]) and ("variable_name" in lowerCaseLines[lineNumber]):
                removeBlock(startOfBlock, lines)
                break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# General function for removing a variable modify definition block in the file
def removeVarModify(keyword):
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()  # This will help with String handling (more stable)
    keyword = keyword.lower()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            if ("variable modify" in lowerCaseLines[startOfBlock + 1]) and ("variable_name" in lowerCaseLines[lineNumber]):
                removeBlock(startOfBlock, lines)
                break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function takes a variable name and removes that variable's create and modify block
def removeVar(keyword):
    removeVarCreate(keyword)
    removeVarModify(keyword)
#-----------------------------------------------------------------------------------------------------------------------
# Replaces a variable with its real value in all instances of the file
def replaceAllVar(varName, realValue):
    # Initialize file reader first ("read and look before you change and write")
    file = open(defeatureFile, "r")
    newLines = ""

    # For every instance the variable is seen, replace it with its real value
    for line in file:
        changes = line.replace(varName, str(realValue))
        newLines = newLines + changes

    file.close()

    # Update those changes to the file with file writer
    updatedFile = open(defeatureFile, "w")
    updatedFile.write(newLines)

    updatedFile.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes a force modify block in the file
def removeForceModify(keyword):
    # Initialize file reader
    file = open(defeatureFile, "r")
    keyword = keyword.lower()
    lines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # Scan through file to find the force modify block we ae looking for (if it is there)
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:  # Keyword will be the name of the force whose modify block you want deleted
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            # The header is always one below the start which is top "!" (changed to include var name check)
            if ("force modify" in lowerCaseLines[startOfBlock + 1]) and ("force_name" in lowerCaseLines[lineNumber]):
                removeBlock(startOfBlock, lines)
                break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Gets the old RP_gearSep equation that is defined
# IMPROVEMENT: Change this to where you scan through the file, and find it by --COMPLETED; SEE V2--
# looking for keywords all in one line ("2", "*", "PI", "ABS", "VARVAL", "VAR_reps_meas_pinionTorque_Nmm", etc.)
def getOldRPGearSepEqu():
    originalEqu = "2* PI * ABS(VARVAL(." + fileName + ".VAR_reps_meas_pinionTorque_Nmm) / ." + fileName + ".repsCalc_rpCFactor * TAN(." + fileName + ".reps_A_rpNormPressAng) / COS(." + fileName + ".repsCalc_rackHelixAng))"
    return originalEqu
#-----------------------------------------------------------------------------------------------------------------------
# Gets the old RP_gearSep equation that is defined in a force modify
# Version 2 of existing method as a more stable and flexible improvement
def getOldRPGearSepEquV2():
    originalEqu = ""
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    keyword = "SFORCE_reps_RP_gearSep"
    keyword = keyword.lower()

    for index, line in enumerate(file):
        line = line.lower()
        # Find the equation's block first by getting its force's name and scanning for corresponding modify block
        if keyword in line:
            endOfBlock = findEndOfBlock(index)  # Index of last "!" in gearSep equation force block
            startOfBlock = findStartOfBlock(endOfBlock) # Index of first or top "!" in gearSep equation force block
            if ("force" in fileLines[startOfBlock+1]) and ("modify" in fileLines[startOfBlock+1]):
                # Index down until we find the line where the equation is
                i = startOfBlock
                while i < endOfBlock:
                    # Find the line where the equation is listed indicated by the "function ="
                    if ("function" in fileLines[i]) and ("=" in fileLines[i]):
                        gearSepFunction = fileLines[i]
                        startSnip = gearSepFunction.find("=") + 1
                        # Checking if we can use a "&" delimiter or not; either way will extract equation
                        if "&" in gearSepFunction:
                            endSnip = gearSepFunction.find("&")
                            gearSepFunction = gearSepFunction[startSnip:endSnip]
                            gearSepFunction = gearSepFunction.strip()
                            gearSepFunction = gearSepFunction.strip('"')
                        else:
                            gearSepFunction = gearSepFunction[startSnip:]
                            gearSepFunction = gearSepFunction.strip()
                            gearSepFunction = gearSepFunction.strip('"')

                        # Store the extracted equation through updating outer equation variable
                        originalEqu = gearSepFunction

                    i = i + 1

    file.close()
    return originalEqu
#-----------------------------------------------------------------------------------------------------------------------
# Gets the new RP_gearSep equation by getting real values and the file name for substitution
def getNewRPGearSepEqu():
    newEqu = "2* PI * ABS(VARVAL(." + fileName + ".VAR_reps_meas_pinionTorque_Nmm) / " + str(getCFactor()) + " * TAN(" + str(getPressAngle()) + "d) / COS(" + str(getHelixAngle()) + "d))"
    return newEqu
#-----------------------------------------------------------------------------------------------------------------------
# Inserts in the new RP_gearSep equation using built-in replace Python function
def insertRPGearSepEqu():
    # Get the old and new gear sep. equations first before replacing
    oldGearSepEqu = getOldRPGearSepEquV2()  # Better method works now
    newGearSepEqu = getNewRPGearSepEqu()

    # Open file reader
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    for ind, line in enumerate(fileLines):
        fileLines[ind] = fileLines[ind].lower()
    newLines = ""
    keyword = "SFORCE_reps_RP_gearSep"
    keyword = keyword.lower()
    foundGearSep = False

    # Scan through lines in file until we find the spot to replace at
    if hasKeyword(keyword, fileLines):
        foundGearSep = True
        for line in file:
            changes = line.replace(oldGearSepEqu, newGearSepEqu)
            newLines = newLines + changes
    else:
        foundGearSep = False
        tkinter.messagebox.showwarning(title="Runtime Warning", message="BTS could not find SFORCE_reps_RP_gearSep in "
                                                                        "the file.\nPlease make sure the naming "
                                                                        "conventions are consistent.")

    file.close()

    if foundGearSep:
        # Open file writer and upload those changes
        updatedFile = open(defeatureFile, "w")
        updatedFile.write(newLines)

        updatedFile.close()
#-----------------------------------------------------------------------------------------------------------------------
# Removes a block that has a repsCalc variable inside of it
def removeRepsCalcVar():
    # Keyword used in Ctrl+F and how program will find block top-down
    keyword = "repsCalc"
    keyword = keyword.lower()

    # Open the CMD file to edit as a TXT file to scan first
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()

    # Scan through file until we find the repsCalc instance, then remove it
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, lines)
            break
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Changes RB Spring Preload variable to its real value in all references to it
def changeRBSpringPreloadToVal():
    fileLines = open(defeatureFile).readlines()

    # We have to make sure it exists before we try to remove and replace it
    if hasKeyword("rackBrgSpr_preload", fileLines):
        RBPreloadFullName = getFullVarName("rackBrgSpr_preload")
        RBPreloadFullName = removeWhiteSpace(RBPreloadFullName)
        RBPreloadRealValue = getRBSpringPreload()
        removeVarCreate("rackBrgSpr_preload")
        replaceAllVar(RBPreloadFullName, RBPreloadRealValue)
    else:
        tkinter.messagebox.showwarning(title="Runtime Warning", message="Variable rackBrgSpr_preload not found. "
                                                                        "\nPlease revise.")
#-----------------------------------------------------------------------------------------------------------------------
# Changes RB Spring Stiffness variable to its real value in all references to it
def changeRBSpringStiffToVal():
    fileLines = open(defeatureFile).readlines()

    # We have to make sure it exists before we try to remove and replace it
    if hasKeyword("rackBrgSpr_stiff", fileLines):
        RBStiffnessFullName = getFullVarName("rackBrgSpr_stiff")
        RBStiffnessFullName = removeWhiteSpace(RBStiffnessFullName)
        RBStiffnessRealValue = getRBSpringStiffness()
        removeVarCreate("rackBrgSpr_stiff")
        replaceAllVar(RBStiffnessFullName, RBStiffnessRealValue)
    else:
        tkinter.messagebox.showwarning(title="Runtime Warning", message="Variable rackBrgSpr_stiff not found.\nPlease "
                                                                        "revise.")
#-----------------------------------------------------------------------------------------------------------------------
# General function for changing instances of a variable to its real value
def changeVarToVal(keyword, hasVarModify=True):
    fileLines = open(defeatureFile).readlines()

    if hasKeyword(keyword, fileLines):
        # Initialize and format
        varFullName = getFullVarName(keyword)
        varFullName = removeWhiteSpace(varFullName)
        varRealValue = getRealValue(varFullName)  # Used to be keyword in ()
        varRealValue = removeWhiteSpace(varRealValue)

        # If the real value has multiple values indicated by a comma, then we use ADAM's CMD array notation
        if "," in varRealValue:
            varRealValue = "{" + varRealValue + "}"

        removeVarCreate(keyword)

        # Check if the keyword variable also has its own variable modify block; if so, remove it
        if hasVarModify:
            removeVarModify(keyword)

        # Once we remove the variable create and modify, replace all references with real values
        replaceAllVar(varFullName, varRealValue)
    else:
        tkinter.messagebox.showwarning(title="Runtime Warning", message="Variable " + keyword + " to replace with its "
                                                                        "real value could not be found in the "
                                                                        "file.\nPlease revise.")
#-----------------------------------------------------------------------------------------------------------------------
# Changes all instances of a specified variable to its respected real values in the file
def changeVarToValAll(keyword):
    currentFile = open(defeatureFile).readlines()
    while hasKeyword(keyword, currentFile):
        changeVarToVal(keyword)
        currentFile = open(defeatureFile).readlines()
#-----------------------------------------------------------------------------------------------------------------------
# Removes all instances and definitions of repsCalc variables in the file
def removeAllRepsCalcVar():
    currentFile = open(defeatureFile).readlines()
    while hasKeyword("repsCalc", currentFile):
        removeRepsCalcVar()
        currentFile = open(defeatureFile).readlines()
#-----------------------------------------------------------------------------------------------------------------------
# Uses the repsCalc keyword to replace all instances of repsCalc with its respected real values
def removeAndReplaceAllRepsCalcVar():
    keyword = "repsCalc"
    changeVarToValAll(keyword)
#-----------------------------------------------------------------------------------------------------------------------
# Finds the total length of a text file
def fileLength(nameOfFile):
    with open(nameOfFile) as f:
        for i, l in enumerate(f):
            pass
    f.close()

    return i + 1   # i will start from 0 in for loop, so add 1 to round to its actual length
#-----------------------------------------------------------------------------------------------------------------------
# This gets the first letter index of a string by searching for the first encountered alphabet instance
def getFirstLetterIndex(string):
    #Initialize index and format string to make checking easier (more flexible)
    string = string.lower()
    indexOfLetter = 0

    # Scan through the string with index and find first alphabet instance
    for index, char in enumerate(string):
        if (char == "a" or char == "b" or char == "c" or char == "d" or char == "e" or char == "f" or char == "g" or
            char == "h" or char == "i" or char == "j" or char == "k" or char == "l" or char == "m" or char == "n" or
            char == "o" or char == "p" or char == "q" or char == "r" or char == "s" or char == "t" or char == "u" or
            char == "v" or char == "w" or char == "x" or char == "y" or char == "z"):
            indexOfLetter = index
            break

    return indexOfLetter
#-----------------------------------------------------------------------------------------------------------------------
# This function finds the last letter index of a segment header by finding where the second half of the indicator is
def getLastLetterIndex(string, startOfFirstLetterIndex):
    endLetterIndex = startOfFirstLetterIndex
    currentChar = ""

    while (currentChar != "!") and (currentChar != "-"):
        currentChar = string[endLetterIndex]
        endLetterIndex = endLetterIndex + 1

    endLetterIndex = endLetterIndex - 1  # This fixed the part name including a "-" in name

    return endLetterIndex
#-----------------------------------------------------------------------------------------------------------------------
# This function finds if a marker is associated or not by seeing if its instance is inside its own block or not
# (Referenced outside = it's associated)
def isAssociatedMarker(keyword):
    # Initialize values
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    isAssociated = False
    keyword = keyword.lower()
    for ind, line in enumerate(fileLines):
        fileLines[ind] = fileLines[ind].lower()

    # Scan through file until we find an instance of the marker's name (keyword) -> determine if associated
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            # If the keyword is in its own header, then it is its own block
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            #if ("marker create" in fileLines[index - 1]) or ("marker attributes" in fileLines[index - 1]):
            # -- IMPROVEMENT COMPLETE -- Changed if statement to better filter unassociativity or self-reference from
            # actual associativity. If statement for being under its own block is now more stable.
            if (("marker create" in fileLines[startOfBlock + 1]) or ("marker attributes" in fileLines[startOfBlock + 1])) and ("marker_name" in line):
                pass
            else:
                isAssociated = True

    file.close()

    return isAssociated
#-----------------------------------------------------------------------------------------------------------------------
# Finds and removes unassociated reps_variables in the file
def findAndRemoveUnassociated():
    # Initialize values and file reader
    unassociatedVars = []
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    for ind, line in enumerate(fileLines):
        fileLines[ind] = fileLines[ind].lower()

    # Scan through the file until we find a variable name (making sure its under a variable create block)
    for index, line in enumerate(file):
        if ("variable_name" in fileLines[index]) and ("variable create" in fileLines[index - 1]):
            # Extract that variable name for processing
            snipStartIndex = line.find("=") + 1
            snipEndIndex = line.find("&")
            fullVarName = line[snipStartIndex:snipEndIndex]
            # Make sure it's a reps_variable by checking
            if (fileName + ".reps_") in fullVarName:
                fullVarName = removeWhiteSpace(fullVarName)
                unassociatedVars.append(fullVarName)

    file.close()

    # Length of unassociatedVars list would be out of range, so we start from the end by one less than the length
    # (Why? Well, in programming, items in lists start at index 0 and go up to one less than the list's length!)
    i = len(unassociatedVars) - 1
    # Simplifying the unassociatedVars array to only include unassociated variables
    # Must start from the end of the unassociated list since we can't cut the tree we are standing on
    while i >= 0:
        # Initialize
        file = open(defeatureFile, "r")
        removed = False

        # Scan through the file with the current reps_variable in hand (using i)
        for index, line in enumerate(file):
            if unassociatedVars[i] in line:
                # If the variable is found in its own modify or create block (one down from header), it checks out
                if ("variable modify" in fileLines[index - 1]) or ("variable create" in fileLines[index - 1]):
                    pass
                # If we find the reps_variable anywhere else, it is actually associated and we must remove it
                else:
                    unassociatedVars.remove(unassociatedVars[i])
                    removed = True
                    break

        # If we remove a variable from the list, reset the counter back to the new end
        if removed:
            i = len(unassociatedVars) - 1

        else:
            i = i - 1

        file.close()

    # For every element or item in the list, perform the removal process for that variable
    for element in unassociatedVars:
        removeVar(element)

#-----------------------------------------------------------------------------------------------------------------------
# This function replaces the remaining associated variables with their real values
# (NOTE: we know they are associated since in top-down order, we already removed the unassociated)
def findAndReplaceAssociated():
    # Initialize values and file reader
    associatedVars = []
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    for ind, line in enumerate(fileLines):
        fileLines[ind] = fileLines[ind].lower()

    # Scan through the file until we find variable name line under the variable create header
    for index, line in enumerate(file):
        if ("variable_name" in fileLines[index]) and ("variable create" in fileLines[index - 1]):
            # Extracting the full variable name process:
            snipStartIndex = line.find("=") + 1
            snipEndIndex = line.find("&")
            fullVarName = line[snipStartIndex:snipEndIndex]

            # Verify it's a reps_variable since that's the type of variable we're after
            if (fileName + ".reps_") in fullVarName:
                fullVarName = removeWhiteSpace(fullVarName)
                associatedVars.append(fullVarName)

    file.close()

    # Append the found (associated) variable names to the list and once all is appended, traverse list and replace
    for element in associatedVars:
        changeVarToValAll(element)
#-----------------------------------------------------------------------------------------------------------------------
# This function removes certain force modifies while keeping ones that should stay by various checks
def removeOtherForceModifies():
    # Initialize file reader and list of what force modifies we will remove in the end
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    forcesToRemove = []

    # Scan through the file until we find a force modify
    for index, line in enumerate(file):
        line = line.lower()
        if "force modify" in line:
            # Check if it's a direct single force (SFORCE), a general force (GFORCE), or misc.
            if "direct single_component_force" in line:
                foundForceName = False
                forceName = ""
                i = index
                # Find the force name through a while loop traversal
                while not foundForceName:
                    if "force_name" in fileLines[i]:
                        # Start to extract the force name if we found it
                        snipStartIndex = fileLines[i].find("=") + 1
                        snipEndIndex = fileLines[i].find("&")
                        forceName = fileLines[i]
                        forceName = forceName[snipStartIndex:snipEndIndex]
                        forceName = removeWhiteSpace(forceName)
                        forceName = forceName.strip()
                        foundForceName = True
                    i = i + 1

                # Check internally if the force name is one we need to keep; else, add it on to remove list
                if ("reps_impct_RackBrg" in forceName) or ("reps_impct_RPbottom" in forceName) or ("reps_RP_gearSep" in forceName) or ("MotorTorque_SysInp_Nmm" in forceName) or ("reps_BScrew_UnsymFr" in forceName) or ("HW_Sens_Unsym_torque" in forceName):
                    pass
                else:
                    forcesToRemove.append(forceName)
            # If it was instead a direct general force, go through similar process
            elif "direct general_force" in line:
                foundForceName = False
                forceName = ""
                i = index
                while not foundForceName:
                    if "force_name" in fileLines[i]:
                        snipStartIndex = fileLines[i].find("=") + 1
                        snipEndIndex = fileLines[i].find("&")
                        forceName = fileLines[i]
                        forceName = forceName[snipStartIndex:snipEndIndex]
                        forceName = removeWhiteSpace(forceName)
                        foundForceName = True
                    i = i + 1
                if "reps_bnutIso_NLspring" in forceName:
                    pass
                else:
                    forcesToRemove.append(forceName)
            # Else it is misc. and thus we don't remove it
            else:
                pass  # This is to ignore the bushings and frictions force modifies

    file.close()

    # Now that you have all the force modifies to remove in the forcesToRemove list, go through and remove
    for element in forcesToRemove:
        removeForceModify(element)

#-----------------------------------------------------------------------------------------------------------------------
# This function extracts the full marker name from a specified line in the file
def getFullMarkerName(startFromIndex):
    # Initialize values
    fileLines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()
    markerName = ""
    foundName = False
    i = startFromIndex
    # While loop until we found the desired name, and make sure it is a marker name
    while not foundName:
        if "marker_name" in lowerCaseLines[i]:
            snipStartIndex = fileLines[i].find("=") + 1
            snipEndIndex = fileLines[i].find("&")
            markerName = fileLines[i]
            markerName = markerName[snipStartIndex:snipEndIndex]
            markerName = removeWhiteSpace(markerName)
            foundName = True
            break

        i = i + 1

    return markerName
#-----------------------------------------------------------------------------------------------------------------------
# This function removes a marker create block of a specified name
def removeMarkerCreate(keyword):
    # Initialize values
    keyword = keyword.lower()
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # Scan through the file
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:  # Keyword will be the name of the marker whose create block you want deleted
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            # The header is always one below the start which is top "!"
            if ("marker create" in lowerCaseLines[startOfBlock + 1]) and ("marker_name" in lowerCaseLines[lineNumber]):
                removeBlock(startOfBlock, lines)
                break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes the marker attributes block of a specified name
def removeMarkerAttr(keyword):
    # Initialize values
    file = open(defeatureFile, "r")
    lines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()
    keyword = keyword.lower()

    # Scan through the file
    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:  # Keyword will be the name of the variable whose create block you want deleted
            lineNumber = index
            endOfBlock = findEndOfBlock(lineNumber)
            startOfBlock = findStartOfBlock(endOfBlock)
            # The header is always one below the start which is top "!"
            # Still using the ping-pong algorithm for removal but with extra check on the block header
            if ("marker attributes" in lowerCaseLines[startOfBlock + 1]) and ("marker_name" in lowerCaseLines[lineNumber]):
                removeBlock(startOfBlock, lines)
                break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes certain markers in the ground FRAME segment
def removeGroundFrameMarkers():
    # Initialize values and file reader
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    lowerCaseLines = open(defeatureFile).readlines()
    markersToRemove = []
    startOfSegment = 0
    endOfSegment = 0
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # Scan through file until we find the stat of the ground frame segment
    for index, line in enumerate(file):
        line = line.lower()
        if ("--- reps_ground_FRAME ---" in line) or ("--- reps_ground_Frame ---" in line) or ("--- reps_ground_frame ---" in line):
            startOfSegment = index  # This will make the starting the segment point where the !-- --! divider is
            endOfSegment = index + 1  # Start the end index one past to not conflict while loop
            foundEnd = False
            # While loop until we find the end of ground frame segment
            while not foundEnd:
                if "!---" in fileLines[endOfSegment]:
                    foundEnd = True
                    break
                endOfSegment = endOfSegment + 1

    file.close()

    # Now we have the start of the ground_FRAME segment and end of the ground_FRAME segment
    i = startOfSegment
    while i < endOfSegment:
        # We scan through each marker inside ground frame and collect those to remove (of no importance)
        if "marker create" in lowerCaseLines[i]:
            currentFoundMarker = getFullMarkerName(i)
            if isAssociatedMarker(currentFoundMarker):
                pass  # pass means "do nothing", indicating this marker is important and to be kept
            elif ("MKR_Bench" in currentFoundMarker) or ("atInpShftTop" in currentFoundMarker) or (("_gearMount_" in currentFoundMarker) and ("ctr" in currentFoundMarker)) or (("_toGearMnt" in currentFoundMarker) and ("_JntRef" in currentFoundMarker)) or ("benchTest" in currentFoundMarker) or ("ITRJ" in currentFoundMarker) or ("Fixt" in currentFoundMarker) or ("fixt" in currentFoundMarker):
                pass
            elif "MASSPROP" in currentFoundMarker:    
                markersToRemove.append(currentFoundMarker)
            elif ("mass" in currentFoundMarker) or ("inertia" in currentFoundMarker):
                pass
            else:
                markersToRemove.append(currentFoundMarker)

        i = i + 1

    # Now we got all the possible markers inside the ground_FRAME segment; start removing markers
    for element in markersToRemove:
        removeMarkerCreate(element)
        removeMarkerAttr(element)
#-----------------------------------------------------------------------------------------------------------------------
# This function finds and removes datum marker and datum attribute blocks
def findAndRemoveDatum():
    # Initialize values
    file = open(defeatureFile, "r")
    listOfDatumMarkers = []

    # Scan through file
    for index, line in enumerate(file):
        line = line.lower()
        # Check if we find a marker create block (if we do, get the name of the marker)
        if "marker create" in line:
            currentFoundMarker = getFullMarkerName(index)

            # Check if the marker name we got is a datum marker by searching for datum keywords
            if "datum" in currentFoundMarker:
                listOfDatumMarkers.append(currentFoundMarker)
            elif "DATUM" in currentFoundMarker:
                listOfDatumMarkers.append(currentFoundMarker)
            elif "Datum" in currentFoundMarker:
                listOfDatumMarkers.append(currentFoundMarker)

    file.close()

    # Whatever we gathered in the list, remove it (both create and attribute blocks)
    for element in listOfDatumMarkers:
        removeMarkerCreate(element)
        removeMarkerAttr(element)
#-----------------------------------------------------------------------------------------------------------------------
# This function finds and removes a parasolid segment instance from the file
def findAndRemoveParasolid():
    # Initialize the values and file reader
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    startOfSegment = 0
    endOfSegment = 0
    foundParasolid = False

    # Scan through file until we find a parasolid segment (if there is one)
    for index, line in enumerate(file):
        line = line.lower()  # This could be useful for flexibility in other code of this script.
        if ("parasolid" in line) and ("!" in line) and ("***" in line):
            foundParasolid = True
            startOfSegment = index
            i = index + 1
            endOfFile = fileLength(defeatureFile)
            # While loop down until we find the end of the parasolid segment where the next segment begins
            while i < endOfFile:
                if ("!---" in fileLines[i]) or ("! ---" in fileLines[i]) or ("! ***" in fileLines[i]) or ("!***" in fileLines[i]):
                    endOfSegment = i
                    break
                i = i + 1

    file.close()

    # Remove the parasolid segment if we found it
    if foundParasolid:
        removeSegment(startOfSegment, endOfSegment, fileLines)
#-----------------------------------------------------------------------------------------------------------------------
# This function removes a single PSMAR block using the block removal process (ping-pong method)
def removePSMAR():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()

    for index, line in enumerate(file):
        line = line.lower()
        if "psmar" in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, fileLines)
            break

    # Close the file to avoid corruption and conflicts.
    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Remove all instances of PSMAR (parasolid markers) in case any remain in the file
def removeAllPSMAR():
    lowerCaseFileLines = open(defeatureFile).readlines()
    for index, line in enumerate(lowerCaseFileLines):
        lowerCaseFileLines[index] = lowerCaseFileLines[index].lower()

    while hasKeyword("psmar", lowerCaseFileLines):
        removePSMAR()
        lowerCaseFileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(lowerCaseFileLines):
            lowerCaseFileLines[ind] = lowerCaseFileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes the model specific colors segment in the file
def removeModelSpecificColors():
    # Initialize values and the file readers
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    endOfFile = fileLength(defeatureFile)
    startOfSegment = 0
    endOfSegment = 0
    found = False

    # Scan through file until the model specific colors segment is found
    for index, line in enumerate(file):
        line = line.lower()
        if ("model specific colors" in line) and ("!---" in line):
            found = True
            startOfSegment = index
            i = index + 1
            # Internally loop through segment to find where the segment ends by finding where the next begins
            while i < endOfFile:
                if ("!---" in fileLines[i]) or ("! ---" in fileLines[i]) or ("!***" in fileLines[i]) or ("! ***" in fileLines[i]):
                    endOfSegment = i
                    break
                i = i + 1

    file.close()

    # If we did find the model specific colors segment (which we should), remove it
    if found:
        removeSegment(startOfSegment, endOfSegment, fileLines)

#-----------------------------------------------------------------------------------------------------------------------
# This function performs a single removal of a benchOC spline block
def removeBenchOCSpline():
    # Initialize file readers
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()

    # Start scanning to find the first encountered benchOC instance (if there is one)
    for index, line in enumerate(file):
        line = line.lower()
        if "benchoc" in line:
            # Ping-pong algorithm, find the end using current, find the start using end, remove using start
            # (Very helpful and used often since starting line is usually unclear)
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, fileLines)
            break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Removes all subsequent benchOC instances in the file using the single removal method as a "cycle"
def removeAllBenchOC():
    lowerCaseFileLines = open(defeatureFile).readlines()
    for index, line in enumerate(lowerCaseFileLines):
        lowerCaseFileLines[index] = lowerCaseFileLines[index].lower()

    while hasKeyword("benchoc", lowerCaseFileLines):
        removeBenchOCSpline()
        lowerCaseFileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(lowerCaseFileLines):
            lowerCaseFileLines[ind] = lowerCaseFileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function checks if a segment is registered in the ground frame (first step to being a part segment)
def isInDefaultGroundFrame(fileLines, startOfSegment):
    index = startOfSegment + 1  # Must start one line past segment header (!--- ---!) so while doesn't end at start
    isInGroundFrame = False
    endOfFile = fileLength(defeatureFile)
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # "While we haven't reached the end", which is the next segment
    while (index < endOfFile) and (("!" not in fileLines[index]) or ("---" not in fileLines[index])):
        if ("default_coordinate_system" in lowerCaseLines[index]) and ("reps_ground_frame" in lowerCaseLines[index]):
            isInGroundFrame = True
            break
        index = index + 1

    return isInGroundFrame
#-----------------------------------------------------------------------------------------------------------------------
# This function checks if a segment has the part create and part name attribute to see if it's a part segment
def isPartSegment(fileLines, startOfSegment, segmentName):
    # Initialize values
    index = startOfSegment + 1  # Start one past so we don't conflict the while loop
    isPart = False
    endOfFile = fileLength(defeatureFile)
    lowerSegmentName = segmentName.lower()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # "While we haven't reached the end AND while we haven't seen both the ! and --- indicators in the same line":
    # (One part of the while is to make sure we aren't at the end, the other is to ensure we haven't hit a segment)
    while (index < endOfFile) and (("!" not in fileLines[index]) or ("---" not in fileLines[index])):
        # If we found the part create block:
        if "part create rigid_body name" in lowerCaseLines[index]:
            blockIndex = index
            # While loop down until we find the line with that has the part name listed
            while "!" not in fileLines[blockIndex]:
                # Try to match the part name with the inputted segment name to verify it's a part segment
                if ("part_name" in lowerCaseLines[blockIndex]) and (lowerSegmentName in lowerCaseLines[blockIndex]):
                    isPart = True
                    break
                blockIndex = blockIndex + 1
        index = index + 1

    return isPart
#-----------------------------------------------------------------------------------------------------------------------
# This function finds a list of part segments that are in the current file
def findPartSegments():
    # Initialize list and file reader
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    partSegments = []

    # Scan through the file
    for index, line in enumerate(file):
        # Find a segment using !--- ---! segment indicators
        if ("!" in line) and ("---" in line):
            startOfSegmentNameIndex = getFirstLetterIndex(line)
            endOfSegmentNameIndex = getLastLetterIndex(line, startOfSegmentNameIndex)
            segmentName = line[startOfSegmentNameIndex:endOfSegmentNameIndex]
            segmentName = removeWhiteSpace(segmentName)
            # Check if the segment is actually a part segment by ground frame and other part attributes
            if (isInDefaultGroundFrame(fileLines, index)) and (isPartSegment(fileLines, index, segmentName)):
                # This .append() method appends the name of the part segment to the list (updating it)
                partSegments.append(segmentName)

    # ALWAYS close the file to prevent file conflicts and errors (you don't do this with .readlines() though)
    file.close()

    return partSegments
#-----------------------------------------------------------------------------------------------------------------------
# This function finds if a part is inside it's own segment by backtracking upwards in the file
def isPartInOwnSegment(partName, indexOfFoundPart, fileLines):
    # Initialize values
    index = indexOfFoundPart
    isPartOfOwnSegment = False
    partName = partName.lower()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    # While loop will stop at nearest segment header, where part reference was found
    while ("!" not in fileLines[index]) or ("---" not in fileLines[index]):
        if index == 0:
            break
        index = index - 1

    # Once we arrived at the segment header, check if it's the part's own segment header
    if partName in lowerCaseLines[index]:
        isPartOfOwnSegment = True

    return isPartOfOwnSegment
#-----------------------------------------------------------------------------------------------------------------------
# This function finds if a part/component is associated by seeing if its instances are inside its own segment
# "If the part is referenced outside = it is associated" type logic
def isPartAssociated(fileLines, partName):
    index = 0
    endOfFile = fileLength(defeatureFile)
    isAssociated = False

    # While loop to index through file lines, looking for the part name
    while index < endOfFile:
        if partName in fileLines[index]:
            snipStart = partName.find(".")
            snipStart = snipStart + 1
            shortPartName = partName[snipStart:]  # Short part name example: Belt vs. (long) reps_11dummy_r1.Belt
            shortPartName = shortPartName.strip()  # Added this to see if prevents Pinion bug association deletion
            # If it's found in its own segment, we don't care. If it ISN'T then we know it's associated.
            if isPartInOwnSegment(shortPartName, index, fileLines):
                pass
            if not isPartInOwnSegment(shortPartName, index, fileLines):
                isAssociated = True
                break
        index = index + 1

    return isAssociated
#-----------------------------------------------------------------------------------------------------------------------
# This function finds the start of a segment using it's segment name (a segment is a larger block with !--- ---!)
def getStartOfSegment(segmentName, fileLines):
    startOfSegment = 0
    index = 0
    endOfFile = fileLength(defeatureFile)
    segmentName = segmentName.lower()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    while index < endOfFile:
        # If we find the inputted segment name and the indicators of a segment, we found our starting point
        if (segmentName in lowerCaseLines[index]) and ("!" in fileLines[index]) and ("---" in fileLines[index]):
            startOfSegment = index
            break
        index = index + 1

    return startOfSegment
#-----------------------------------------------------------------------------------------------------------------------
# This function finds the end of a segment using it's starting point
def getEndOfSegment(startOfSegment, fileLines):
    # Initialize starting values
    endOfSegment = 0
    index = startOfSegment + 1
    endOfFile = fileLength(defeatureFile)

    while index < endOfFile:
        # If we find the next segment indicators, we know we reached the end of THIS segment
        if ("!" in fileLines[index]) and ("---" in fileLines[index]):
            endOfSegment = index
            break
        index = index + 1

    return endOfSegment
#-----------------------------------------------------------------------------------------------------------------------
# This function filters out associated part segments and removes those that are are unassociated
def removeUnassociatedPartSegments():
    # Initialize default values
    fileLines = open(defeatureFile).readlines()
    allPartSegments = findPartSegments()
    totalParts = len(allPartSegments)
    partRemoved = False

    i = 0
    # While loop for going through list of part segments (for loop wasn't good enough for this one)
    while i < totalParts:
        # Reset values if removal happened
        if partRemoved:
            i = 0
            totalParts = len(allPartSegments)
            # Reset the flag as well
            partRemoved = False
        # Filter out the parts that ARE associated first
        fullPartName = fileName + "." + allPartSegments[i]
        if isPartAssociated(fileLines, fullPartName):
            allPartSegments.remove(allPartSegments[i])
            partRemoved = True
        i = i + 1

    # Remove each segment according to remaining parts in the list
    for element in allPartSegments:
        startIndex = getStartOfSegment(element, fileLines)
        endIndex = getEndOfSegment(startIndex, fileLines)
        removeSegment(startIndex, endIndex, fileLines)
#-----------------------------------------------------------------------------------------------------------------------
# This function removes a single instance of a DATA REF axial spring block
def removeDataRefAxialSprNL():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    keyword = "DATA_REF_reps_axialSprNL"
    keyword = keyword.lower()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            # We check if it's a create block by looking one down from the starting block index which is a "!"
            if "data_element create" in lowerCaseLines[startOfBlock + 1]:
                removeBlock(startOfBlock, fileLines)
                break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Removes all subsequent instances of a DATA REF axial spring block
def removeAllDataRefAxialSprNL():
    keyword = "DATA_REF_reps_axialSprNL"
    keyword = keyword.lower()
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword(keyword, fileLines):
        removeDataRefAxialSprNL()
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes a single instance of a DATA WIP1 spring block
def removeWIPBenchSprNL():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    keyword = "DATA_WIP1_benchSprNL"
    keyword = keyword.lower()
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            # We check if it's a create block by looking one down from the starting block index which is a "!"
            if "data_element create" in lowerCaseLines[startOfBlock + 1]:
                removeBlock(startOfBlock, fileLines)
                break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Removes all subsequent instances of a DATA WIP1 block
def removeAllWIPBenchSprNL():
    keyword = "DATA_WIP1_benchSprNL"
    keyword = keyword.lower()
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword(keyword, fileLines):
        removeWIPBenchSprNL()
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function performs a single removal of a direct object AVG block
def removeDOBJAvg():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    keyword = "DOBJ_avg"
    keyword = keyword.lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, fileLines)
            break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function performs a single removal of a direct object RMS block
def removeDOBJRms():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    keyword = "DOBJ_rms"
    keyword = keyword.lower()

    for index, line in enumerate(file):
        line = line.lower()
        if keyword in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, fileLines)
            break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes all direct object AVG blocks from file (Brett requires others to stay)
def removeAllDOBJAvg():
    keyword = "DOBJ_avg"
    keyword = keyword.lower()
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword(keyword, fileLines):
        removeDOBJAvg()
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function removes all direct object RMS blocks from file (Brett requires others to stay)
def removeAllDOBJRms():
    keyword = "DOBJ_rms"
    keyword = keyword.lower()
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword(keyword, fileLines):
        removeDOBJRms()
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# A key function of the program to get the model name of from the file using Adams View Model segment
def getActualModelName():
    # Initialize variables to start from beginning
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    endOfFile = fileLength(defeatureFile)
    lowerCaseLines = open(defeatureFile).readlines()
    for ind, line in enumerate(lowerCaseLines):
        lowerCaseLines[ind] = lowerCaseLines[ind].lower()
    i = 0
    modelName = ""
    foundModelName = False

    # Start scanning through file to find View Model segment where the model name is given
    for index, line in enumerate(file):
        line = line.lower()
        if ("!" in line) and ("---" in line) and ("adams view model" in line):
            # Once we found it, while loop down until we come across the line where the model name is listed
            i = index
            while i < endOfFile:
                if "model_name" in lowerCaseLines[i]:
                    snipStart = fileLines[i].find("=") + 1
                    # Have two cases: one if & sign is there, and one if & sign is not there
                    if "&" in fileLines[i]:
                        snipEnd = fileLines[i].find("&")
                        modelName = fileLines[i]
                        modelName = modelName[snipStart:snipEnd]
                        modelName = removeWhiteSpace(modelName)
                        foundModelName = True
                        break
                    else:
                        modelName = fileLines[i]
                        modelName = modelName[snipStart:]
                        modelName = removeWhiteSpace(modelName)
                        foundModelName = True
                        break
                # Increment while loop with i (allows for termination, so no infinite loop).
                i = i + 1

        # If we found the model name, break out to save us some work.
        # Note that the model name will always be in the model file, so no else case is needed
        if foundModelName:
            break

    file.close()

    modelName = modelName.strip()

    return modelName
#-----------------------------------------------------------------------------------------------------------------------
# Removes a measure block based on if the specified measure is found
def removeMeasure(measureType):
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()
    measureType = measureType.lower()

    for index, line in enumerate(file):
        line = line.lower()
        # This should take care of both measure create blocks and attributes block
        if measureType in line:
            endOfBlock = findEndOfBlock(index)
            startOfBlock = findStartOfBlock(endOfBlock)
            removeBlock(startOfBlock, fileLines)
            break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Repeats removal process for measures for all subsequent specified instances
def removeAllMeasure(measureType):
    measureType = measureType.lower()
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword(measureType, fileLines):
        removeMeasure(measureType)
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function accounts for if a specific color remains referenced after model specific colors removal process
def replaceSpecificColor():
    file = open(defeatureFile, "r")
    fileLines = open(defeatureFile).readlines()

    # Scan through the file, see if we find a specific model color indicated by the COLOR_ prefix
    for index, line in enumerate(file):
        line = line.lower()
        if "color_" in line:
            fullColorName = fileLines[index]
            snipStart = fileLines[index].find("=") + 1
            # If we do find an instance, handle it according to if a & is present or not. Replaces with color RED.
            if "&" in line:
                snipEnd = fileLines[index].find("&")
                fullColorName = fullColorName[snipStart:snipEnd]
                fullColorName = removeWhiteSpace(fullColorName)
                replaceAllVar(fullColorName, "RED")
                break
            else:
                fullColorName = fullColorName[snipStart:]
                fullColorName = fullColorName.strip()
                fullColorName = removeWhiteSpace(fullColorName)
                replaceAllVar(fullColorName, "RED")
                break

    file.close()
#-----------------------------------------------------------------------------------------------------------------------
# Repeats specific color removal process for all subsequent instances
def replaceAllSpecificColors():
    fileLines = open(defeatureFile).readlines()
    for index, line in enumerate(fileLines):
        fileLines[index] = fileLines[index].lower()

    while hasKeyword("color_", fileLines):
        replaceSpecificColor()
        fileLines = open(defeatureFile).readlines()
        for ind, line in enumerate(fileLines):
            fileLines[ind] = fileLines[ind].lower()
#-----------------------------------------------------------------------------------------------------------------------
# This function checks over all initial components and segments in the model to see if any are too short
# (Too short component names can cause unexpected results in the output, a name at least 4 characters is advised)
def checkComponentNames():
    file = open(defeatureFile, "r")
    isAllGood = True

    # Scan through file until reach a segment indicator, then see if the segment's name is too small
    # There are default Adams segments, but manual component segments are what we're after here.
    # There have been no instances thus far that a default Adams segment is shorter than 4 characters, so it works
    for index, line in enumerate(file):
        if ("!" in line) and ("---" in line):
            startOfSegmentNameIndex = getFirstLetterIndex(line)
            endOfSegmentNameIndex = getLastLetterIndex(line, startOfSegmentNameIndex)
            segmentName = line[startOfSegmentNameIndex:endOfSegmentNameIndex]
            segmentName = removeWhiteSpace(segmentName)
            if len(segmentName) <= 3:
                # Having a component be less than 4 letters long can cause the script to be confused in removals
                isAllGood = False
                break

    file.close()

    return isAllGood
#-----------------------------------------------------------------------------------------------------------------------
# Makes a backup file of the original source file in the same directory
def backupSourceFile():
    sourceFile = defeatureFile
    targetFile = r"" + backupFile + ""
    shutil.copyfile(sourceFile, targetFile)
#-----------------------------------------------------------------------------------------------------------------------
# This function provides the browse files window functionality to the "Browse..." button in the GUI
def browseFiles(display):
    # This is a built-in tool to bring up the browse files window, added arguments to only choose TXT files
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File To Defeature",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ))
    # Reference the global file variable to store outside the chosen file. Then, display the chosen file in entry.
    global chosenFile
    chosenFile = filename
    setEntryText(chosenFile, display)

    # This is inserted here to make check method below work, still the same "get" from what's in entry box
    global defeatureFile
    defeatureFile = chosenFile
    defeatureFile = r"" + defeatureFile + ""

    # If checking component names results in a not good check:
    if not checkComponentNames():
        tkinter.messagebox.showwarning(title="Model Warning", message="A component in the selected model has too "
                                                                      "short of a name.\nThis may cause unexpected "
                                                                      "results in removal.\nPlease revise.")
    if fileIsEmpty(defeatureFile):
        display.delete(0, END)
        tkinter.messagebox.showerror(title="Critical Warning", message="The selected file is empty.\nPlease revise or "
                                                                       "select a different model.")
#-----------------------------------------------------------------------------------------------------------------------
# This function will check if an entry box is empty or not (an entry box is the text field you see in the GUI)
def isEmptyBox(entry):
    isEmpty = False

    # "len()" is used to get the length of the string in the entry field. If it's 0, well then it's empty.
    if len(entry.get()) == 0:
        isEmpty = True

    return isEmpty
#-----------------------------------------------------------------------------------------------------------------------
# This function will check and process if all data gathered from the entry boxes are sufficient to execute main()
def okButtonPressed(root, defeatureEntry, backupEntry, messageWindowLabel):
    # Initialize outer variables with default values
    readyToExecute = False
    isBoxEmpty = False
    global defeatureFile

    # Get the defeature file name which is the full file path displayed
    defeatureFile = defeatureEntry.get()

    # Check if nothing is in the entry box, if so we can't execute
    if isEmptyBox(defeatureEntry):
        isBoxEmpty = True
    elif defeatureEntry.get() == "No File Chosen":
        isBoxEmpty = True

    # Gather the data and format to be precise, use that data to check extension is TXT
    defeatureFile = r"" + defeatureFile + ""
    defeatureFile = defeatureFile.strip('"')
    defeatureFileName = os.path.basename(defeatureFile)
    isDefeatureReady = True
    invalidExtensionPresent = False
    defeatureExtensionIndex = defeatureFileName.find(".")
    defeatureExtension = defeatureFileName[defeatureExtensionIndex:]
    if defeatureExtension != ".txt":
        invalidExtensionPresent = True

    # Move on the backup entry box and get what's inside the entry field
    global backupFile
    backupFileName = backupEntry.get()

    # Check if it's empty; if so, we can't execute
    if isEmptyBox(backupEntry):
        isBoxEmpty = True

    # If user provided no extension in the naming of the backup file, add the .txt for them
    if (".txt" not in backupFileName) and ("." not in backupFileName):
        backupFileName = backupFileName + ".txt"

    isBackupReady = True

    # Check for the valid TXT extension if user DID provide an extension
    if "." in backupFileName:
        extensionIndex = backupFileName.find(".")
        extension = backupFileName[extensionIndex:]
        if extension != ".txt":
            invalidExtensionPresent = True

    # If we got an invalid extension, proceed with alert and abort process
    if invalidExtensionPresent:
        backupEntry.delete(0, END)
        defeatureEntry.delete(0, END)
        isBackupReady = False
        isDefeatureReady = False
        messageWindowLabel.config(text="ERROR: Invalid extension. \nPlease do not include any extensions except "
                                       ".txt in the backup file "
                                       "name. \nYou may just input the backup file name and the .txt will be added on "
                                       "automatically. \nAlso, double check that the defeature file is a .txt as "
                                       "well.")
        invalidExtensionPresent = False

    # If we have an empty entry box (the GUI text boxes), proceed with alert and abort process
    if isBoxEmpty:
        backupEntry.delete(0, END)
        defeatureEntry.delete(0, END)
        isBackupReady = False
        isDefeatureReady = False
        messageWindowLabel.config(text="ERROR: Both fields must be filled before starting.\nPlease go back and select "
                                       "your file to defeature and\nenter the name of the backup file.")
        invalidExtensionPresent = False
        isBoxEmpty = False

    # If everything checks out, we are at a "go-ahead" to execute
    if (isBackupReady) and (isDefeatureReady):
        defeatureFile = r"" + defeatureFile + ""
        defeaturePath = os.path.dirname(defeatureFile)
        backupFile = r"" + defeaturePath + "\\" + backupFileName + ""

        readyToExecute = True

    # If given the "go-ahead" to execute, do it!
    if readyToExecute:
        startProcessWindow(root)

#-----------------------------------------------------------------------------------------------------------------------
# The third and final GUI window for displaying a loading bar that tracks defeature progress
def startProcessWindow(oldRoot):
    # Switches to this loading bar window
    oldRoot.quit()
    secondRoot = Toplevel()

    # Divide GUI window into 2 frames, one for the banner header and the other for the loading bar
    frame1 = Frame(secondRoot)
    frame2 = Frame(secondRoot)

    # Below are widgets used in this process GUI window: banner, icon, title, loading bar, loading label
    img = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerBannerBTS.png")
    imageLabel = Label(frame1, image=img)
    imageLabel.pack()

    secondRoot.iconbitmap(r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerIcon.ico")

    secondRoot.title("BTS 3000 - Defeaturer")

    progressLabel = Label(frame2, text="Defeaturing...")

    progressBar = ttk.Progressbar(frame2, orient=HORIZONTAL, length=600, mode="determinate")
    progressBar["maximum"] = 100

    # Inserting or packing all widgets into the GUI window (smaller widgets packed first, then frames)
    progressBar.pack()
    progressLabel.pack()
    frame1.pack()
    frame2.pack()

    # Execute the main defeature process in the background, using its steps to update the loading bar
    try:
        main(progressBar, progressLabel)
    except FileNotFoundError:
        secondRoot.withdraw()
        tkinter.messagebox.showerror(title="Model Error", message="Could not find the selected model file.\nPlease "
                                                                  "make sure either the file exists \nor is in the "
                                                                  "correct directory.")

    # This loop keeps the GUI running
    secondRoot.mainloop()
#-----------------------------------------------------------------------------------------------------------------------
# Modifies an entry box's text to the passed in text
def setEntryText(text, entry):
    entry.delete(0, "end")
    entry.insert(0, text)
#-----------------------------------------------------------------------------------------------------------------------
# Removes extra spaces from a string
def removeWhiteSpace(string):
    return string.replace(" ", "")
#-----------------------------------------------------------------------------------------------------------------------
# File length function produces incorrect result in the case of an empty file. This function compensates for it.
def fileIsEmpty(path):
    isFileEmpty = False
    fileSize = os.path.getsize(path)

    if fileSize == 0:
        isFileEmpty = True

    return isFileEmpty
#-----------------------------------------------------------------------------------------------------------------------
# The main function to be used in the main method.
def main(progress, statusLabel):
    # Perform main operations here:
    # Added parameters and extra calls to provide GUI loading bar display

    # Make an initial backup source file before de-featuring the current one
    statusLabel.config(text="Backing up source file...")
    backupSourceFile()
    progress['value'] += 2
    progress.update()

    # WORKS NOW; changes fileName to correct model name just in case of different file name
    global fileName
    fileName = getActualModelName()
    # This step doesn't count towards progress

    # Eliminating all cylinder creations with automatic updating and removal
    statusLabel.config(text="Removing cylinders...")
    removeAllCylinders()
    progress['value'] += 2

    # Reset current file read status to start eliminating all cylinder references in markers
    statusLabel.config(text="Removing cylinder references...")
    removeAllCylinderRefs()
    progress['value'] += 2
    progress.update()

    # Reset current file read status to start eliminating all marker modify blocks
    statusLabel.config(text="Removing marker modifies...")
    removeAllMarkerModifies()
    progress['value'] += 2
    progress.update()

    # Replaces CFactor, PressAngle, and HelixAngle variables with their real values in RPGearSep equation
    statusLabel.config(text="Replacing RPGearSep equation with real values...")
    insertRPGearSepEqu()
    progress['value'] += 2
    progress.update()

    # Eliminating all repsCalc design variables INCLUDING the variable modify blocks since they have same pattern
    #removeAllRepsCalcVar() [old and obsolete method; removeAndReplaceAllRepsCalcVar is the better one; tested & works]
    statusLabel.config(text="Removing and replacing all REPS Calc variables...")
    removeAndReplaceAllRepsCalcVar()
    progress['value'] += 4.5
    progress.update()
    # NOTE that the remove repsCalc func removes ALL blocks that have a repsCalc variable in them

    # Change rack bearing spring preload and stiffness from variables to real values in other blocks
    # Also deletes the old variable create definitions since were changed to numbers.
    statusLabel.config(text="Changing rack bearing spring preload to real value...")
    changeRBSpringPreloadToVal()  # CONFIRMED METHOD TO TURN FILE INTO BINARY 0's = FIXED!
    progress['value'] += 4.5
    progress.update()

    statusLabel.config(text="Changing rack bearing spring stiffness to real value...")
    changeRBSpringStiffToVal()  # ALSO CONFIRMED METHOD TO TURN FILE INTO BINARY 0's = FIXED!
    progress['value'] += 4.5
    progress.update()

    # Changes all variable references to repsUser_K and M to values stored in K and M (all mounts and bnuts)
    statusLabel.config(text="Replacing REPS User K references with real values...")
    changeVarToValAll("repsUser_K")
    progress['value'] += 4.5
    progress.update()

    statusLabel.config(text="Replacing REPS User M references with real values...")
    changeVarToValAll("repsUser_M")
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; Will find unassociated reps_variables and then delete them
    statusLabel.config(text="Removing unassociated REPS variables...")
    findAndRemoveUnassociated()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; After removing unassociated, will find and replace all associated reps_variables
    statusLabel.config(text="Removing and replacing associated REPS variables...")
    findAndReplaceAssociated()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; Removes other unwanted force modifies as listed per Removing Parameters documentation
    statusLabel.config(text="Removing specific force modifies...")
    removeOtherForceModifies()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes unassociated ground markers, non-location ground markers, and non-mass/inertia markers
    # Bug that some of marker attributes don't get deleted - FIXED
    statusLabel.config(text="Removing certain ground FRAME markers...")
    removeGroundFrameMarkers()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; finds and remove datum marker blocks
    statusLabel.config(text="Removing datum blocks...")
    findAndRemoveDatum()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; finds and removes parasolid graphic segment in file if there is one
    statusLabel.config(text="Removing parasolid graphics...")
    findAndRemoveParasolid()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes model specific colors segment at the top of CMD file
    statusLabel.config(text="Removing model specific colors...")
    removeModelSpecificColors()
    replaceAllSpecificColors()  # Added this to replace any possible remaining specific colors in model.
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all benchOC-type spline blocks (along with all blocks referring to a benchOC spline)
    statusLabel.config(text="Removing benchOC-type splines...")
    removeAllBenchOC()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all unassociated component segments of CMD file (parasolid-related/PSMAR)
    statusLabel.config(text="Removing unassociated components...")
    removeUnassociatedPartSegments()  # --NOTE-- This is what was causing the all lower case in file issue
    removeAllPSMAR()  # This executes after removing part segments in case any PSMARs left
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all DataREF Axial Spring NL blocks (iter1, iter2, etc.)
    statusLabel.config(text="Removing DataREF Axial Spring blocks...")
    removeAllDataRefAxialSprNL()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all WIP1 Bench Spring NL blocks
    statusLabel.config(text="Removing WIP Bench Spring blocks...")
    removeAllWIPBenchSprNL()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all DOBJ Average blocks (objectives)
    statusLabel.config(text="Removing all DOBJ average blocks...")
    removeAllDOBJAvg()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all DOBJ RMS blocks (objectives)
    statusLabel.config(text="Removing all DOBJ rms blocks...")
    removeAllDOBJRms()
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all calcErr-type MEAS from model file
    statusLabel.config(text="Removing calcErr MEAS measures...")
    removeAllMeasure("MEAS_calcErr")
    progress['value'] += 4.5
    progress.update()

    # WORKS NOW; removes all testRef-type MEAS from model file
    statusLabel.config(text="Removing testRef MEAS measures...")
    removeAllMeasure("MEAS_testRef")
    progress['value'] += 4.5
    progress.update()

    # Update messenger in GUI to alert user that the defeature is complete (Smiley face is a must for satisfaction)
    statusLabel.config(text="Defeature process complete. :)\nYour defeatured model can be found at:\n" + defeatureFile)
#-----------------------------------------------------------------------------------------------------------------------
def mainGUI():
    try:
        # Destroy the temporary splash GUI frame (forms a "transition"-like animation to GUI)
        splashFrame.destroy()

        # Initialize the main frame.
        rootFrame = Tk()

        # Initial window settings
        #rootFrame.geometry("580x450")
        rootFrame.state("zoomed")

        # Background being setup
        img3 = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerBannerBckgrnd.png")
        imageLabelBackground = Label(rootFrame, image=img3)
        imageLabelBackground.place(x=0, y=0, relwidth=1, relheight=1)

        # Frames to be used in root; frame 1 is the header Nexteer banner while frame 2 has the widgets
        frame1 = Frame(rootFrame)

        frame2 = Frame(rootFrame)

        # Setting up banner images, icons, and titles for first main window
        img = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerBannerBTS.png")
        imageLabelHeader = Label(frame1, image=img)
        imageLabelHeader.pack()
        rootFrame.iconbitmap(r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerIcon.ico")
        rootFrame.title("BTS 3000 - Defeaturer")

        # Setting up the widgets
        defeatureEntry = Entry(frame2)
        backupEntry = Entry(frame2)
        fileChosenLabel = Label(frame2, text="Defeature File", width=50, height=3)
        backupFileLabel = Label(frame2, text="Backup File", width=50, height=3)
        messageWindowLabel = Label(frame2, text="")
        okButton = Button(frame2, text="OK", height=2, width=5, command=lambda: threading.Thread(target=okButtonPressed(rootFrame, defeatureEntry, backupEntry, messageWindowLabel)).start())
        fileExploreButton = Button(frame2, text="Browse...", command=lambda: browseFiles(defeatureEntry))

        # Inserting widgets using grid formatting
        okButton.grid(row=3, column=4)
        defeatureEntry.grid(row=1, column=2)
        fileExploreButton.grid(row=1, column=3)
        fileChosenLabel.grid(row=1, column=1)
        backupEntry.grid(row=2, column=2)
        backupFileLabel.grid(row=2, column=1)
        messageWindowLabel.grid(row=3, column=2)

        # Set the entry text to initially no file chosen to hint the user to selecting a file from Browse...
        setEntryText("No File Chosen", defeatureEntry)

        # Pack the frames and make the header span across X-window while frame2 spans as far down Y as possible
        frame1.pack(fill="x", anchor="center")
        frame2.pack(fill="y", anchor="center")

        # This loop keeps the GUI running
        rootFrame.mainloop()
    except TclError:
        # Pop up an error window
        tkinter.messagebox.showerror(title="GUI Error", message="There's an issue with one or more of the GUI "
                                                                "components.\nPlease check that you connected to your "
                                                                "drive where the GUI files are and nothing is missing in BTS3000_GUI_Files.")
#-----------------------------------------------------------------------------------------------------------------------
# The main method to execute this Python script only
if __name__ == "__main__":
    try:
        # Splash frame that appears while main screen still boots up
        splashFrame = Tk()
        splashFrame.geometry("300x350")
        splashFrame.overrideredirect(1)
        splashFrame.title("")
        splashFrame.iconbitmap(r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerIcon.ico")

        # Center the splash frame window on screen
        splashFrame.eval("tk::PlaceWindow . center")

        # Adding these widgets to the splash screen:
        img = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\NexteerBannerBTS.png")
        imageLabelHeader = Label(splashFrame, image=img)
        imageLabelHeader.pack(ipady=25)

        loadImg = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\Loading_Circle (1).png")
        #loadImg = PhotoImage(file=r"Drive:\[YOUR]\[GUI_Files]\[DIRECTORY]\[HERE]\blah.jpg")  # Raises TK error; DONT USE JPG
        loadImageLabel = Label(splashFrame, image=loadImg)
        loadImageLabel.pack(ipady=45)

        # Splash screen will last for 5 seconds before going away (the main GUI window will take its place)
        splashFrame.after(5000, mainGUI)

        mainloop()
    except TclError:
        # Pop up an error window
        tkinter.messagebox.showerror(title="GUI Error", message="There's an issue with one or more of the GUI "
                                                                "components.\nPlease check that you connected to your "
                                                                "drive where the GUI files are and nothing is missing in BTS3000_GUI_Files.")
