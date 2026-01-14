#!/bin/bash
REPORT_FILE="report.md"
echo "# T-Pipes Verification Report" > $REPORT_FILE
echo "**Date:** $(date)" >> $REPORT_FILE
echo "" >> $REPORT_FILE

run_check() {
    NAME=$1
    CMD=$2
    echo "## Checking: $NAME" >> $REPORT_FILE
    echo "Command: \`$CMD\`" >> $REPORT_FILE
    echo "" >> $REPORT_FILE
    
    # Capture output and exit code
    OUTPUT=$(eval $CMD 2>&1)
    EXIT_CODE=$?
    
    # Write output block
    echo "\`\`\`" >> $REPORT_FILE
    echo "$OUTPUT" >> $REPORT_FILE
    echo "\`\`\`" >> $REPORT_FILE
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "" >> $REPORT_FILE
        echo "**RESULT:** ✅ PASS" >> $REPORT_FILE
    else
        echo "" >> $REPORT_FILE
        echo "**RESULT:** ❌ FAIL" >> $REPORT_FILE
    fi
    echo "" >> $REPORT_FILE
    echo "---" >> $REPORT_FILE
}

run_check "Unit Tests" "venv/bin/python tests_blocks.py -v"
run_check "JSON Pipeline (example.yaml)" "venv/bin/python main.py run example.yaml --refresh"
run_check "XML Pipeline (example_xml.yaml)" "venv/bin/python main.py run example_xml.yaml --refresh"
run_check "HTML Pipeline (example_html.yaml)" "venv/bin/python main.py run example_html.yaml --refresh"
run_check "Export Pipeline (example_export.yaml)" "venv/bin/python main.py run example_export.yaml --refresh"

echo "Verification Complete. Report saved to [$REPORT_FILE]($REPORT_FILE)"
