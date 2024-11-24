*** Settings ***
Library    Process
Library    OperatingSystem

*** Variables ***
${GAME_SCRIPT}    C:/Users/attem/OneDrive/Työpöytä/Python game/Snake.py

*** Test Cases ***
Game Starts Correctly
    [Documentation]    Testaa, että peli käynnistyy ilman virheitä.
    Start Game Process
    Check If Game Process Is Running

*** Keywords ***
Start Game Process
    Start Process    python    ${GAME_SCRIPT}    stdout=output.txt    stderr=output.txt

Check If Game Process Is Running
    Wait For Process    # Odottaa, että prosessi on suoritettu ja ei kaadu
    ${output}=    Get File    output.txt
    Should Not Contain    ${output}    Traceback
    Should Not Contain    ${output}    Error
