<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    
    <!-- We need a separator here, otherwise we can't tell the difference between e.g. 1,20 and 12,0 -->
    <xsl:key name="locations-by-coords" match="location" use="concat(x, ',', y)" />
    
    <!-- Only match reservoirs that have at least one location after stripping duplicates -->
    <xsl:template match="reservoir[count(location[generate-id() = generate-id(key('locations-by-coords', concat(x, ',', y))[1])]) != 0]" mode="secondPass">
        <xsl:copy>
            <!-- Iterate over the unique locations in a reservoir -->
            <xsl:apply-templates select="location[generate-id() = generate-id(key('locations-by-coords', concat(x, ',', y))[1])]" mode="secondPass" />
        </xsl:copy>
    </xsl:template>
    
    <!-- Actually output the location -->
    <xsl:template match="location" mode="secondPass">
        <xsl:copy-of select="." />
    </xsl:template>
    
</xsl:stylesheet>