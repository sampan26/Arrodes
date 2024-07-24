"use client";
import { useState } from "react";
import {
  Alert,
  Button,
  FormControl,
  FormLabel,
  Heading,
  HStack,
  Icon,
  Input,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Stack,
  Tag,
  Table,
  Textarea,
  Thead,
  Tbody,
  Th,
  Tr,
  Text,
  useDisclosure,
  FormHelperText,
  FormErrorMessage,
} from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { TbPlus, TbInfoCircle } from "react-icons/tb";
import { useForm } from "react-hook-form";
import API from "@/lib/api";
import { analytics } from "@/lib/analytics";
import { getPromptVariables, DEFAULT_PROMPT } from "@/lib/prompts";
// import PromptRow from "./_components/row";

export default function PromptsClientPage({ data, session }) {
    console.log("===================================================")
    console.log(data)
    console.log("===================================================")
    const { isOpen, onClose, onOpen } = useDisclosure();
    const [selectPrompt, setSelectedPrompt] = useState();
    const router = useRouter();
    const api = new API(session);  
    const {
        formState: { isSubmitting, errors },
        handleSubmit,
        register,
        reset,
        setValue,
        watch,
      } = useForm({
        values: {
          template: DEFAULT_PROMPT,
        },
      });

      const template = watch("template");

      const onSubmit = async (values) => {
        const payload = {
            ...values,
            input_variables: getPromptVariables(values.template) || [],
        }

        if (selectPrompt) {
            await api.patchPrompt(selectPrompt, payload);

            analytics.track("Updated Prompt", { ...payload });
        } else {
            await api.createPrompt(payload);

            analytics.track("Created Prompt", { ...payload });
        }
        
        router.refresh();
        reset();
        setSelectedPrompt();
        onClose();
      }

      const handleDelete = async (promptId) => {
        api.deletePrompt(promptId);

        analytics.track("Deleted Prompt", { id });
        router.refresh();

      }

      const handleEdit = async (promptId) => {
        const prompt = data.find(({ id }) => id === promptId)

        setSelectedPrompt(promptId);
        setValue("name", prompt?.name);
        setValue("template", prompt?.template);
        onOpen();
      }

      return (
        <Stack flex={1} paddingX={12} paddingY={12} spacing={6}>
            <HStack justifyContent="space-between">
                <Stack>
                    <Heading as="h1" fontSize="2xl">
                        Prompts
                    </Heading>
                    <Text color="gray.400">
                        A prompt is piece of text that gives context to the LLM. It can
                        contain instructions on how the Agent should act.
                    </Text>
                </Stack>
                <Button
                    leftIcon={<Icon as={TbPlus} />}
                    alignSelf="flex-start"
                    onClick={onOpen}
                >
                    New Prompt
                </Button>
            </HStack>
            <Stack spacing={4}>
                <Table variant="simple">
                <Thead>
                    <Tr>
                    <Th>Name</Th>
                    <Th>Inputs</Th>
                    <Th>&nbsp;</Th>
                    </Tr>
                </Thead>
                
                </Table>
            </Stack>
        </Stack>
      )
}