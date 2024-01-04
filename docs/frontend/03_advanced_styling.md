# Responsive design
   
In the world of Nextpy, every component is designed with responsiveness at its core, ensuring that your application looks and works great across all devices. The framework provides an arsenal of tools to tweak the responsiveness of your app, allowing for meticulous adjustments that cater to different screen sizes and create a truly adaptable user interface.  
   
## 1. Dynamic Responsiveness
   
Nextpy enables developers to define styles that automatically adjust to various screen sizes, facilitated by a set of predefined breakpoints. This feature allows you to specify a list of style values that correspond to different screen widths, giving you the power to craft an application that not only responds to screen changes but also transforms in appearance to enhance user experience.  
   
For example, to change the text color based on screen size, you can do the following:  
   
```python  
xt.text(  
    "Chameleon text colors",  
    color=["orange", "red", "purple", "blue", "green"],  # Adapts color to screen size  
)  
```  
   
Nextpy's default breakpoints are as follows:  
   
```python  
"sm": '30em',  # Targets small screens, In this example it will show orange
"md": '48em',  # Targets medium screens  
"lg": '62em',  # Targets large screens  
"xl": '80em',  # Targets extra-large screens  
"2xl": '96em',  # Targets extra-extra-large screens, In this example it will show green
```  
   
These breakpoints are the pivot points where your style adaptations kick in, ensuring a smooth transition between different device displays.  
   
## 2. Conditional Component Display  
   
With Nextpy, you can selectively show or hide components depending on the screen size, making use of conditional rendering to tailor the user experience. This is done using helper components that encapsulate the logic required for display conditions, saving you the hassle of writing complex media queries.  
   
Here's how you can use conditional rendering for different views:  
   
```python  
xt.vstack(  
    xt.desktop_only(xt.text("Visible on Desktop")),  
    xt.tablet_only(xt.text("Visible on Tablet")),   
)  
```  
   
This approach allows you to maintain a clean and organized codebase while providing different content or layout optimizations for various device types.  
   
## 3. Hiding Components
   
Nextpy goes beyond the standard breakpoints by giving developers the freedom to define custom display behaviors . The `display` style property can be tuned to determine when a component should be shown or hidden, offering even finer control over the responsiveness of the application.  
   
For instance, showing text only on extra-extra-large screens can be achieved as follows:  
   
```python  
xt.text(  
    "Exclusive for XXL Screens",  
    color="green",  
    display=["none", "none", "none", "none", "block"],  # Appears only on 2xl screens  
)  
```  
   
This level of customization ensures that you can design for specific use cases and audience preferences, optimizing the interface for the exact screen sizes your users are most likely to employ.  
   
## Key Takeaways  
   
Nextpy's responsive design features bring a wealth of benefits for developers aiming to create adaptable and accessible web applications:  
   
- Built-in responsive design ensures that Nextpy components are automatically adjusted for different devices.  
- Dynamic style properties and predefined breakpoints allow for smooth style transitions between screen sizes.  
- Conditional component display provides the flexibility to show or hide elements based on the device's screen size.  
- Customizable breakpoints enable developers to set their own conditions for responsiveness, tailoring the app to specific requirements.  

# Custom Stylesheets

Nextpy empowers you to create visually appealing and brand-aligned apps with tailored styling options. This guide covers how to apply custom stylesheets and fonts to enhance your app's design.  
   
## External Stylesheets  
   
- **Access established design libraries or frameworks:**  
  - Provide the stylesheet URL within the `xt.App` object:  
   
```python  
app = xt.App(  
    stylesheets=[  
        "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.2/css/bootstrap.min.css",  
    ],  
)  
```  
   
## Local Stylesheets  
   
- **Create custom styles for your app:**  
  - Place stylesheets in the `assets/` directory.  
  - Reference them in the `xt.App` object:  
   
```python  
app = xt.App(  
    stylesheets=[  
        "styles.css",  # Path relative to assets/  
    ],  
)  
```  

  
# Custom Fonts  
   
### External Fonts  
   
- **Utilize fonts from services like Google Fonts:**  
  - Specify the font family directly in component properties:  
   
```python  
xt.text(  
    "Check out my IBM Dlex MONO font",  
    font_family="Inter",  # Font from Google Fonts  
    font_size="1.5em",  
)  

app = xt.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap",  # This path is relative to assets/
    ],
)
```  
   
### Local Fonts 
   
#### 1. Font Storage  
   
- Place your custom fonts within the `assets/fonts` directory for easy organization.  
   
#### 2. Stylesheet Creation  
   
- Define font faces within a CSS stylesheet to make them accessible to your app:  
   
```css  
/* myfont.css */  
@font-face {  
  font-family: MyFont;  
  src: url("./MyFont.otf") format("opentype"); /* Relative path to font file */  
}  
   
/* Include bold weight if available */  
@font-face {  
  font-family: MyFont;  
  font-weight: bold;  
  src: url("./MyFont.otf") format("opentype");  
}  
```  
   
#### 3. Stylesheet Integration  
   
- Link the stylesheet to your app using the `stylesheets` parameter within `xt.App`:  
   
```python  
app = xt.App(  
  stylesheets=[  
    "fonts/myfont.css"  
  ]  
)  
```  
   
#### 4. Font Usage in Components  
   
- Employ the font family name in component properties for seamless application:  
   
```python  
xt.text(  
  "This text showcases my custom font!",  
  font_family="MyFont"  
)  
```  
   
### Key Points  
   
- Ensure correct file paths within the CSS to accurately locate your fonts.  
- Consider varying font weights (e.g., bold) for enhanced styling options.  
- Adapt font file extensions (e.g., .ttf, .woff, .woff2) to match your specific font files.  
   
### Additional Tips  
   
- Optimize font loading for performance by using font formats like WOFF or WOFF2.  
- Explore web font optimization techniques for further enhancements.  

   
