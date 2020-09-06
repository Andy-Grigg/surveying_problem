<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:exsl="http://exslt.org/common"
    exclude-result-prefixes="xs exsl"
    version="1.0">
    
   <xsl:include href="firstPass.xslt" />
   <xsl:include href="secondPass.xslt" />
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="grid">
        <!-- Actually implement the logic -->
        <xsl:variable name="firstPass">
            <xsl:apply-templates select="el" mode="first" />
        </xsl:variable>
        
        <!-- Strip duplicate locations and empty reservoirs -->
        <xsl:variable name="reservoirs">
            <xsl:apply-templates select="exsl:node-set($firstPass)/reservoir" mode="secondPass"/>
        </xsl:variable>
                
        <!-- Generate summary results -->
        <xsl:element name="results">
            <xsl:element name="numberOfReservoirs">
                <xsl:value-of select="count(exsl:node-set($reservoirs)/reservoir)" />
            </xsl:element>
            <xsl:element name="reservoirs">
                <xsl:apply-templates select="exsl:node-set($reservoirs)/reservoir" mode="results" />
            </xsl:element>
        </xsl:element>
        
    </xsl:template>
    
    <!-- Results wrapper template -->
    <xsl:template match="reservoir" mode="results">
        <xsl:copy>
            <xsl:attribute name="size">
                <xsl:value-of select="count(location)" />
            </xsl:attribute>
            <xsl:copy-of select="location"/>
        </xsl:copy>
    </xsl:template>
    

</xsl:stylesheet>