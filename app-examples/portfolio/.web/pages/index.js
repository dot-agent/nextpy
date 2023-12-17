

import "focus-visible/dist/focus-visible"
import { Fragment, useContext } from "react"
import { EventLoopContext } from "/utils/context"
import { Event, isTrue, set_val } from "/utils/state"
import { Box, Button, Image, Input, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Text, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextHead from "next/head"



export default function Component() {
  const [addEvents, connectError] = useContext(EventLoopContext);

  return (
    <Fragment>
  <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <Modal isOpen={connectError !== null}>
  <ModalOverlay>
  <ModalContent>
  <ModalHeader>
  {`Connection Error`}
</ModalHeader>
  <ModalBody>
  <Text>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getEventURL().href}
</Text>
</ModalBody>
</ModalContent>
</ModalOverlay>
</Modal>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Fragment>
  <Box className={`flex items-center justify-between mt-5 mx-5 md:mx-10`}>
  <Text>
  {`Logo`}
</Text>
  <Box className={`flex items-center gap-5 `}>
  <Text sx={{"cursor": "pointer"}}>
  {`About`}
</Text>
  <Text sx={{"cursor": "pointer"}}>
  {`Work`}
</Text>
  <Text sx={{"cursor": "pointer"}}>
  {`Contact`}
</Text>
</Box>
</Box>
  <Fragment>
  <Box className={`flex flex-col md:flex-row  items-center justify-evenly mx-5  md:mx-8 mt-16  md:mt-24    `}>
  <Box sx={{"variant": "unstyled", "spacing": "0.5em", "alignItems": "left", "fontSize": "2em"}}>
  <Text className={`md:mb-8 mb-4 text-base md:text-lg`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold"}}>
  {`Branding | Image making `}
</Text>
  <Text className={`md:text-7xl text-3xl`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold"}}>
  {`Visual Designer`}
</Text>
  <Text className={`pt-2 md:text-sm max-w-md text-xs`} sx={{"fontFamily": "Epilogue"}}>
  {`This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com`}
</Text>
  <Button className={` py-8 mt-6 hover:bg-[#2D2D2D]  text-base md:text-lg`} sx={{"bg": "#2D2D2D", "color": "white", "width": "30%", "borderRadius": null, "_hover": {"bg": "#2D2D2D"}}}>
  {`Contact`}
</Button>
</Box>
  <Box className={`flex justify-center items-center`} sx={{"fontSize": "15.25px", "color": "#E3E3E3"}}>
  <Image className={`w-3/6 md:w-4/6`} src={`/image.png`}/>
</Box>
</Box>
</Fragment>
  <Box>
  <VStack className={`flex mb-12 `}>
  <Text className={`text-center md:text-3xl mt-16 md:mt-24 font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Latest work`}
</Text>
  <Box className={`grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 md:pt-4 pt-2  gap-6`}>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/book.jpg`}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/abstract.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/magzine.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/isalah.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/book2.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/book3.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/magzine.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image className={`w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80`} src={`/abstract.jpg`} sx={{"objectFit": "cover"}}/>
  <Text className={`py-2 lg:text-base text-sm font-bold`} sx={{"fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text className={`text-xs md:text-sm`} sx={{"fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
</Box>
</VStack>
</Box>
  <Box className={`flex flex-col md:flex-row items-center justify-evenly gap-4 md:gap-8 mx-5  md:mx-8  pt-2 md:pt-12 lg:pt-14 pb-12 md:pb-20`}>
  <Box>
  <Text className={`md:mb-8 mb-4 text-base md:text-2xl lg:text-3xl`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold"}}>
  {`Lets work together`}
</Text>
  <Text className={`md:mb-8 mb-4 text-sm lg:text-base max-w-lg`} sx={{"fontFamily": "Epilogue"}}>
  {`This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com`}
</Text>
  <Box className={`flex  items-center gap-4 `}>
  <Image className={`w-7 h-7 md:w-9 md:h-9`} src={`/discord.svg`} sx={{"objectFit": "cover"}}/>
  <Image className={` w-7 h-7 md:w-9 md:h-9`} src={`/facebook.svg`} sx={{"objectFit": "cover"}}/>
  <Image className={`w-7 h-7 md:w-9 md:h-9`} src={`/dribbble.svg`} sx={{"objectFit": "cover"}}/>
  <Image className={`w-7 h-7 md:w-9 md:h-9`} src={`/nstagram.svg`} sx={{"objectFit": "cover"}}/>
  <Image className={`w-7 h-7 md:w-9 md:h-9`} src={`/behance.svg`} sx={{"objectFit": "cover"}}/>
</Box>
</Box>
  <Box sx={{"variant": "unstyled", "spacing": "0.5em", "alignItems": "left", "fontSize": "2em"}}>
  <Input className={`mb-2`} placeholder={`Name`} sx={{"_placeholder": {"color": "#2D2D2D"}, "bg": "#F3F3F3", "borderRadius": null, "height": "3rem"}} type={`text`}/>
  <Input placeholder={`Email`} sx={{"_placeholder": {"color": "#2D2D2D"}, "bg": "#F3F3F3", "borderRadius": null, "height": "3rem"}} type={`text`}/>
  <Button className={`mt-6 py-8 text-base md:text-lg`} sx={{"bg": "#2D2D2D", "color": "white", "width": "30%", "borderRadius": null, "_hover": {"bg": "#2D2D2D"}}}>
  {`Submit`}
</Button>
</Box>
</Box>
</Fragment>
  <NextHead>
  <title>
  {`Nextpy App`}
</title>
  <meta content={`A Nextpy app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
