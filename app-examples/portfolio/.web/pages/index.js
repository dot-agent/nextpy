

import "focus-visible/dist/focus-visible"
import { Fragment, useContext } from "react"
import { EventLoopContext } from "/utils/context"
import { Event, isTrue } from "/utils/state"
import { Box, Button, Center, Image, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Text, VStack } from "@chakra-ui/react"
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
  <Fragment>
  <Box className={`flex flex-col md:flex-row items-center justify-center`} sx={{"marginTop": "6rem"}}>
  <VStack alignItems={`left`} spacing={`0.5em`} sx={{"fontSize": "2em"}}>
  <Text className={`md:mb-8 mb-4 text-xs md:text-base`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold"}}>
  {`Branding | Image making `}
</Text>
  <Text className={`md:text-5xl text-3xl`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold", "lineHeight": "1px"}}>
  {`Visual`}
</Text>
  <Text className={`md:text-5xl text-3xl`} sx={{"fontFamily": "Epilogue", "fontWeight": "bold"}}>
  {`Designer`}
</Text>
  <Text className={`pt-2`} sx={{"fontSize": "12.705px", "fontFamily": "Epilogue"}}>
  {`This is a template Figma file, turned into`}
</Text>
  <Text sx={{"lineHeight": "5px", "fontSize": "12.705px", "fontFamily": "Epilogue"}}>
  {`code using Anima.`}
</Text>
  <Text sx={{"fontSize": "12.705px", "fontFamily": "Epilogue"}}>
  {`Learn more at AnimaApp.com`}
</Text>
  <Button variant={`unstyled`}>
  <Center className={`mt-6`} sx={{"bg": "#2D2D2D", "color": "white", "width": "60%", "py": "12px", "borderRadius": null}}>
  {`Contact`}
</Center>
</Button>
</VStack>
  <Box>
  <Center className={`mt-20 md:mt-0 lg:mt-0`} sx={{"fontSize": "15.25px", "color": "#E3E3E3"}}>
  <Image src={`/image.png`} sx={{"width": "50%"}}/>
</Center>
</Box>
</Box>
</Fragment>
  <Box>
  <VStack className={`flex justify-center mb-12`}>
  <Text className={` text-center mt-12 md:mt-20 font-bold`} sx={{"fontSize": "16px", "fontFamily": "Epilogue"}}>
  {`Latest work`}
</Text>
  <Box className={`grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 md:pt-4 pt-2 gap-4`}>
  <Box>
  <Image src={`/book.jpg`} sx={{"width": "159.477px", "height": "159.477"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/abstract.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/magzine.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/isalah.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/book2.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/book3.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/magzine.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
  <Box>
  <Image src={`/abstract.jpg`} sx={{"width": "159.477px", "height": "159.477", "objectFit": "cover"}}/>
  <Text className={`py-2`} sx={{"fontSize": "9.665px", "fontFamily": "Epilogue"}}>
  {`Project title`}
</Text>
  <Text sx={{"fontSize": "8.215px", "fontFamily": "Epilogue"}}>
  {`UI, Art drection`}
</Text>
</Box>
</Box>
</VStack>
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
