# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy!."""

from portfolio import styles

import nextpy as xt

class Header:
    def __init__(self) -> None:
        self.header = xt.center(
            width = '100%',
        )
        self.nav_items: dict(str, str) = {'Home':'#FF6000', 'About':'' , 'Resume':'', 'Project':'', 'Contact':''}
        # self.theme = xt.color_mode_button(
        #     xt.color_mode_icon(),
        #     color_scheme="gray",
        #     _light={"color": "black"},
        #     _dark = {"color": "white"}
        # )

    def grid_items(self, nav_item):
        return (
                xt.grid_item(
                    xt.button(
                        nav_item[0],
                        class_name = 'text-white font-["Mukta", sans-serif]'
                    ),
                    class_name = 'bg-['+f'{nav_item[1]}'+'] m-auto rounded-[50px]'
                )
        )
    
    def navbar(self):
        grid_items = [self.grid_items(nav_item) for nav_item in self.nav_items.items()]
        return xt.grid(
                grid_items[0],
                grid_items[1],
                grid_items[2],
                grid_items[3],
                grid_items[4],
                template_columns="repeat(5, 1fr)",
                gap=[2,6,20,32,40],
                class_name = 'bg-black rounded-[50px] mt-[2em] p-1.5 h-min w-min'
            )
        
    def compile_component(self) -> list[xt.Hstack]:
        return [
            self.navbar(),
        ]
    
    def build(self) -> xt.Component:
        self.header.children = self.compile_component()
        return self.header
    
    
class Main:
    def __init__(self) -> None:
        self.main = xt.center(
            width = "100vw",
            class_name = 'm-4'
        )
        
    def home(self):
        return xt.box(
            xt.vstack(
                xt.spacer(),
                xt.text(
                    'Hello!',
                    class_name = 'py-1 px-2 border border-black rounded-[50px] text-black font-normal'
                ),
                xt.spacer(),
                xt.text(
                    xt.span("I'm "),
                    xt.span(
                        "Jenny",
                        class_name = 'text-[#FF6000]'  
                    ),
                    class_name = 'text-black text-[3em] font-semibold'
                ),
                xt.text(
                    'Product Designer',
                    class_name = 'text-black text-[3em] font-semibold'
                )
            ),
            xt.hstack(
                xt.wrap(
                    xt.image( src = '/quotes.png', width = '10px'),
                    xt.text( 'Jenny\'s exceptional product design ensure our website\'s success. Highly Recommended' ),
                        class_name = 'w-[22vw] text-black font-normal'
                ),
                xt.vstack(
                    xt.image(
                        src = '/semicircle.svg',
                        class_name = 'absolute bottom-0'
                    ),
                    xt.image(
                        src = '/girl.png',
                        class_name = 'absolute bottom-0 h-[48vh]'
                    ),
                    class_name = 'w-[30vw] relative bottom-[-25vh]'
                ),
                xt.wrap(
                    xt.text('Jenny\'s exceptional product design ensure our website\'s success. Highly Recommended' ),
                    class_name = 'w-[22vw] text-black font-normal'
                ),
                width = '100vw',
                class_name = 'h-[50vh] justify-evenly relative'
            ),
            class_name = '100vw m-0'
        )

    def build(self) -> xt.Box:
        self.main.children = [self.home()]
        return self.main
        
class Footer:
    def __init__(self) -> None:
        self.footer = xt.hstack(style = styles.footer_style)
        self.footer.children.append(
            xt.text("© 2023 Ivan Martinez", font_size = "10px", font_weight="bold")
        )
    
    def build(self):
        return self.footer

@xt.page("/", "Landing page")
def landing() -> xt.Component:
    header: object = Header().build()
    main: object = Main().build()
    footer: object = Footer().build()
    return xt.vstack(
        header,
        main,
        # footer,
        class_name = 'bg-white overflow-x-hidden'
    )


app = xt.App(style = styles.app_general_style)



