<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="timeduty">

<SalaryData <xsl:value-of select>>
<body>
<ul>
    <xsl:for-each select="timereport/reportrow">
        <li><xsl:value-of select="username"/></li>
    </xsl:for-each>
</ul>
</body>
</html>   

</xsl:template>

</xsl:stylesheet>