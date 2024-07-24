"use client";
import {
  Button,
  HStack,
  Icon,
  Link,
  Tag,
  Text,
  useColorModeValue
} from "@chakra-ui/react";
import NextLink from "next/link";
import { TbArrowRight } from "react-icons/tb";
import { SUPERAGENT_VERSION } from "@/lib/constants";

export default function MainNav() {


  const fontColor = useColorModeValue("white", "white");

  return (
    <HStack paddingY={6} justifyContent="space-between">
      <HStack spacing={4}>
      <Text as="strong" color={fontColor} fontSize="lg">
        Arrodes
      </Text>
      <Tag size="sm">{SUPERAGENT_VERSION}</Tag>
      </HStack>
      <HStack>
        <Link href="https://discord.gg" color={fontColor}>
          Discord
        </Link>
        <Link href="https://github.com" color={fontColor}>
          Github
        </Link>
        <Link
          color={fontColor}
          href="https://github.com/homanp/superagent/blob/main/.github/CONTRIBUTING.md"
        >
          Contribute
        </Link>
        <Link color={fontColor} href="https://docs.arrodes.sh">
          Docs
        </Link>
        <NextLink passHref href="/login">
          <Button
            rightIcon={<Icon as={TbArrowRight}/>}
            colorScheme="whiteAlpha"
            backgroundColor="white"
          >
            Login
          </Button>
        </NextLink>
      </HStack>
    </HStack>
  )
}