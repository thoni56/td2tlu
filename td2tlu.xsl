<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="timeduty">

<SalaryData>
    <TimeCodes>
    </TimeCodes>
    <SalaryDataEmployee FromDate="" ToDate="">
        <xsl:for-each select="timereport/reportrow">
            <TimeCode>
                <xsl:value-of select="username"/>
            </TimeCode>
        </xsl:for-each>
    </SalaryDataEmployee>
</SalaryData>

</xsl:template>

</xsl:stylesheet>