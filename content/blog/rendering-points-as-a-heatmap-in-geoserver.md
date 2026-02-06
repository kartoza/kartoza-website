---
title: "Rendering Points as a Heatmap in GeoServer"
description: "A brief walk through on how an SLD to render a Heatmap with Labelled Clusters was made for GeoServer."
tags:
  - GeoServer
  - SLD
  - Mapping
date: 2025-01-17
author: "Jeremy Prior"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Rendering Points as a Heatmap in GeoServer"
    subtitle="GeoServer"
    class="is-primary"
    sub-block-side="bottom"
>}}
A brief walk through on how an SLD to render a Heatmap with Labelled Clusters was made for GeoServer.
{{< /block >}}

## Rendering Points as a Heatmap in GeoServer

A task involved rendering a points layer as a heatmap on GeoServer. The client provided QGIS styling they wanted replicated using an SLD (Styled Layer Descriptor). Direct export from QGIS to SLD failed because the generated file contained:

```xml
<!--FeatureRenderer heatmapRenderer not implemented yet-->
```

This indicated the style was essentially non-renderable.

## Initial Solution

Consultation of the [GeoServer Styling Manual](https://docs.geoserver.org/latest/en/user/styling/index.html#styling) revealed documentation on heatmap generation using rendering transformations. Using the provided example as a foundation, adjustments were made to meet client requirements.

**Initial heatmap style parameters:**
- `weightAttr` set as `geometry` for point weighting
- `radiusPixels` set to 75 (controls heatmap spread)
- `pixelsPerCell` set to 5 (higher resolution)
- Color ramp from white through blue, cyan, red, orange, to yellow
- Opacity set to 0.5

Key modifications included adjusting radius and resolution values, adding color stops, and matching hex codes to client specifications.

**Challenge encountered:** GeoServer's built-in style previewer did not accurately display heatmap styling, requiring front-end testing after each modification.

## Enhanced Solution: Heatmap with Labeled Clusters

The client requested additional functionality: displaying relative counts of heatmap surfaces. This prompted research into similar implementations. Finding none, a custom solution using Point Stacker logic was developed.

**Clustering approach:**
- Based on simplified Point Stacker transformation
- `cellSize` parameter set to 20 map units
- `count` property filtered to display only clusters with 5+ points (reducing visual clutter)
- White Arial Bold labels with black halos for readability

**Critical discovery:** The two transformation logics (heatmap and clustering) required separate `FeatureTypeStyle` elements. Additionally, heatmap styling must be declared first in the SLD.

## Final Combined SLD Structure

The complete style combines both elements:

1. **First FeatureTypeStyle:** Heatmap rendering transformation with rasterized color mapping
2. **Second FeatureTypeStyle:** Point stacking with conditional text labeling

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
  xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
  xmlns="http://www.opengis.net/sld"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <Name>Cluster points</Name>
    <UserStyle>
      <Title>Clustered points</Title>
      <Abstract>Styling using cluster points server side</Abstract>

      <!-- Heatmap FeatureTypeStyle -->
      <FeatureTypeStyle>
        <Transformation>
          <ogc:Function name="vec:Heatmap">
            <ogc:Function name="parameter">
              <ogc:Literal>data</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>weightAttr</ogc:Literal>
              <ogc:Literal>geometry</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>radiusPixels</ogc:Literal>
              <ogc:Literal>75</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>pixelsPerCell</ogc:Literal>
              <ogc:Literal>5</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputBBOX</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_bbox</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputWidth</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_width</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputHeight</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_height</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
          </ogc:Function>
        </Transformation>
        <Rule>
          <RasterSymbolizer>
            <Geometry>
              <ogc:PropertyName>geometry</ogc:PropertyName>
            </Geometry>
            <Opacity>0.5</Opacity>
            <ColorMap type="ramp">
              <ColorMapEntry color="#FFFFFF" quantity="0" label="" opacity="0"/>
              <ColorMapEntry color="#4444FF" quantity=".1" label=""/>
              <ColorMapEntry color="#00FFAE" quantity=".3" label=""/>
              <ColorMapEntry color="#FF0000" quantity=".5" label="" />
              <ColorMapEntry color="#FFAE00" quantity=".75" label=""/>
              <ColorMapEntry color="#FFFF00" quantity="1.0" label="" />
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>

      <!-- Clustering and labeling logic -->
      <FeatureTypeStyle>
        <Transformation>
          <ogc:Function name="gs:PointStacker">
            <ogc:Function name="parameter">
              <ogc:Literal>data</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>cellSize</ogc:Literal>
              <ogc:Literal>20</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputBBOX</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_bbox</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputWidth</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_width</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>outputHeight</ogc:Literal>
              <ogc:Function name="env">
                <ogc:Literal>wms_height</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
          </ogc:Function>
        </Transformation>
        <Rule>
          <Name>Clusters</Name>
          <Title>Clusters</Title>
          <ogc:Filter>
            <ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyName>count</ogc:PropertyName>
              <ogc:Literal>5</ogc:Literal>
            </ogc:PropertyIsGreaterThanOrEqualTo>
          </ogc:Filter>
          <TextSymbolizer>
            <Label>
              <ogc:PropertyName>count</ogc:PropertyName>
            </Label>
            <Font>
              <CssParameter name="font-family">Arial</CssParameter>
              <CssParameter name="font-size">10</CssParameter>
              <CssParameter name="font-weight">bold</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0</AnchorPointX>
                  <AnchorPointY>0</AnchorPointY>
                </AnchorPoint>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>0.4</Radius>
              <Fill>
                <CssParameter name="fill">#000000</CssParameter>
                <CssParameter name="fill-opacity">1</CssParameter>
              </Fill>
            </Halo>
            <Fill>
              <CssParameter name="fill">#FFFFFF</CssParameter>
              <CssParameter name="fill-opacity">1.0</CssParameter>
            </Fill>
          </TextSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
```

## Results and Future Improvements

The completed style renders points as a heatmap with overlaid cluster labels showing counts. The client approved the functional result. However, the author notes intentions to revisit the labeling logic to better align cluster labels with heatmap color breaks rather than relying on separate clustering logic.
