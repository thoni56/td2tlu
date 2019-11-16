<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output indent="yes" />

    <xsl:template match="timeduty">
        <xsl:variable name="fromTime" select="/timeduty/settings/setting[@name='FilterDateFrom']/@value"></xsl:variable>
        <xsl:variable name="fromDate" select="substring($fromTime, 1, 10)"></xsl:variable>
        <xsl:variable name="toTime" select="/timeduty/settings/setting[@name='FilterDateTo']/@value"></xsl:variable>
        <xsl:variable name="toDate" select="substring($toTime, 1, 10)"></xsl:variable>
        <SalaryData>
            <TimeCodes>
            </TimeCodes>
            <SalaryDataEmployee FromDate="{$fromDate}" ToDate="{$toDate}">
                <xsl:for-each select="timereport/reportrow">
                    <xsl:sort select="username"/>
                    <xsl:sort select="date"/>
                    <Employee>
                        <xsl:value-of select="username"/>
                        <xsl:value-of select="date"/>
                    </Employee>
                </xsl:for-each>
            </SalaryDataEmployee>
        </SalaryData>

    </xsl:template>

</xsl:stylesheet>