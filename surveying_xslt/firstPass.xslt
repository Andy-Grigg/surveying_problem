<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:exsl="http://exslt.org/common"
    exclude-result-prefixes="xs exsl"
    version="1.0">
    
    <!-- First time through we need to create the reservoir element -->
    <xsl:template match="el" mode="first">        
        <xsl:element name="reservoir">

                <xsl:element name="location">
                    <xsl:copy-of select="*" />
                </xsl:element>
                
                <xsl:variable name="this_x" select="number(x/text())"/>
                <xsl:variable name="this_y" select="number(y/text())"/>
                
                <!-- Register that we have visited this element before -->
                <xsl:variable name="visited">
                    <xsl:copy-of select="." />
                </xsl:variable>
                
                <!-- We rely on the grid being sorted in increasing x and y. -->
                <!-- The first time through, we will only find a neighbor with increasing or same x -->
                <xsl:apply-templates select="following::el[
                    (x = $this_x and y = $this_y + 1) or
                    (x = $this_x + 1 and y = $this_y - 1) or
                    (x = $this_x + 1 and y = $this_y) or
                    (x = $this_x + 1 and y = $this_y + 1)]" mode="recursive">
                    <xsl:with-param name="visited" select="$visited" />
                </xsl:apply-templates>
            
        </xsl:element>
    </xsl:template>
    
    <!-- Subsequent times through we don't, but we do need to check we haven't been here before -->
    <xsl:template match="el" mode="recursive">
        <xsl:param name="visited" />
        
        <xsl:variable name="currentElement" select="." />
        
        <!-- Check if we have been here before, which stops infinite recursion -->
        <xsl:if test="not(exsl:node-set($visited)/el[x = $currentElement/x][y = $currentElement/y])">
            
            <xsl:variable name="this_x" select="number(x/text())"/>
            <xsl:variable name="this_y" select="number(y/text())"/>
            
            <!-- Add the current location to the list of visited locations -->
            <xsl:variable name="newVisited">
                <xsl:copy-of select="exsl:node-set($visited)/el" />
                <xsl:copy-of select="$currentElement" />
            </xsl:variable>
            
            <xsl:element name="location">
                <xsl:copy-of select="*" />
            </xsl:element>
            
            <!-- Apply this template over all neighbor locations -->
            <!-- Here we might need to go 'up' and 'left', so we need to check negative offsets -->
            <xsl:apply-templates select="../el[
                (x = $this_x - 1 and y = $this_y - 1) or
                (x = $this_x - 1 and y = $this_y) or
                (x = $this_x - 1 and y = $this_y + 1) or
                (x = $this_x and y = $this_y - 1) or
                (x = $this_x and y = $this_y + 1) or
                (x = $this_x + 1 and y = $this_y - 1) or
                (x = $this_x + 1 and y = $this_y) or
                (x = $this_x + 1 and y = $this_y + 1)]" mode="recursive">
                <xsl:with-param name="visited" select="$newVisited" />
            </xsl:apply-templates>
            
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>