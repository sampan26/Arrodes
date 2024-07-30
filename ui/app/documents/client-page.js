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
  Select,
  Text,
  useDisclosure,
  FormHelperText,
  FormErrorMessage,
  IconButton,
  useToast,
  Box,
  Tag,
  SimpleGrid,
  Textarea,
  Center,
  Spinner,
} from "@chakra-ui/react";
import dayjs from "dayjs";
import NextImage from "next/image";
import { useRouter } from "next/navigation";
import { TbPlus, TbCopy, TbTrash } from "react-icons/tb";
import { useForm } from "react-hook-form";
import API from "@/lib/api";
import { analytics } from "@/lib/analytics";
import { usePsychicLink } from "@psychic-api/link";
import SearchBar from "../_components/search-bar";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);

function DocumentCard({ id, name, createdAt, type, url, onDelete }) {
  const toast = useToast();
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);

    toast({
      description: "Copied to clipboard",
      position: "top",
      colorScheme: "gray",
    });
  };

  return (
    <Stack borderWidth="1px" borderRadius="md" padding={4}>
      <HStack justifyContent="space-between" flex={1}>
        <Text noOfLines={1} as="b" flex={1}>
          {name}
        </Text>
        <Text fontSize="sm" color="gray.500">
          {dayjs(createdAt).fromNow()}
        </Text>
      </HStack>
      <Text fontSize="sm" color="gray.500">
        {`Id: ${id}`}
      </Text>
      <HStack justifyContent="space-between" justifySelf="flex-end">
        <Tag variant="subtle" colorScheme="green" size="sm">
          {type}
        </Tag>
        <HStack spacing={0}>
          <IconButton
            size="sm"
            variant="ghost"
            icon={<Icon color="gray.500" fontSize="lg" as={TbCopy} />}
            onClick={() => copyToClipboard(id)}
          />
          <IconButton
            size="sm"
            variant="ghost"
            icon={<Icon fontSize="lg" as={TbTrash} color="gray.500" />}
            onClick={() => onDelete(id)}
          />
        </HStack>
      </HStack>
    </Stack>
  );
}

export default function DocumentsClientPage({ data, session }) {
  const [filteredData, setData] = useState();
  const [isCreatingDocument, setIsCreatingDocument] = useState();
  const { isOpen, onClose, onOpen } = useDisclosure();
  const router = useRouter();
  const api = new API(session);
  const toast = useToast();
  const {
    formState: { isSubmitting, errors },
    handleSubmit,
    register,
    reset,
    watch,
  } = useForm();

  const documentType = watch("type");
  const { open, isReady, isLoading } = usePsychicLink(
    process.env.NEXT_PUBLIC_PSYCHIC_PUBLIC_KEY,
    async (newConnection) => {
      setIsCreatingDocument(true);
      await api.createDocument({
        name: `Psychic: ${newConnection.connectorId}`,
        type: "PSYCHIC",
        metadata: {
          connectorId: newConnection.connectorId,
        },
      });

      toast({
        description: "Psychic connection created!",
        position: "top",
        colorScheme: "gray",
      });

      setData();
      onClose();
      setIsCreatingDocument();
      router.refresh();
    }
  );
  const shouldShowPsychic = process.env.NEXT_PUBLIC_PSYCHIC_PUBLIC_KEY;

  const onSubmit = async (values) => {
    const { type, name, url, auth_type, auth_key, auth_value } = values;
    const payload = {
      name,
      type,
      url,
      authorization: auth_key && {
        type: auth_type,
        key: auth_key,
        value: auth_value,
      },
    };

    await api.createDocument(payload);

    if (process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY) {
      analytics.track("Created Document", { ...payload });
    }

    toast({
      description: "Document created",
      position: "top",
      colorScheme: "gray",
    });

    setData();
    router.refresh();
    reset();
    onClose();
  };

  const handleDelete = async (id) => {
    await api.deleteDocument({ id });

    if (process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY) {
      analytics.track("Deleted Document", { id });
    }

    toast({
      description: "Document deleted",
      position: "top",
      colorScheme: "gray",
    });
    setData();
    router.refresh();
  };

  const onConnectAPI = async () => {
    open(session.user.user.id);
  };

  const handleSearch = ({ searchTerm }) => {
    if (!searchTerm) {
      setData(data);
    }

    const keysToFilter = ["name", "type"];
    const filteredItems = data.filter((item) =>
      keysToFilter.some((key) =>
        item[key].toString().toLowerCase().includes(searchTerm.toLowerCase())
      )
    );

    setData(filteredItems);
  };

  return (
    <Stack
      flex={1}
      paddingX={[6, 12]}
      paddingY={12}
      spacing={6}
      overflow="auto"
    >
      <HStack justifyContent="space-between" spacing={12}>
        <Stack>
          <Heading as="h1" fontSize="2xl">
            Documents
          </Heading>
          <Text color="gray.400" display={["none", "block"]}>
            Upload documents and use them to do question answering.
          </Text>
        </Stack>
        <Button
          leftIcon={<Icon as={TbPlus} />}
          alignSelf="flex-start"
          onClick={onOpen}
        >
          New document
        </Button>
      </HStack>
      <SearchBar
        onSearch={(values) => handleSearch(values)}
        onReset={() => setData(data)}
      />
      <Stack spacing={4}>
        <SimpleGrid columns={[1, 2, 2, 4]} gap={6}>
          {filteredData
            ? filteredData?.map(({ id, name, createdAt, type, url }) => (
                <DocumentCard
                  key={id}
                  id={id}
                  createdAt={createdAt}
                  name={name}
                  url={url}
                  type={type}
                  onDelete={(id) => handleDelete(id)}
                />
              ))
            : data?.map(({ id, name, createdAt, type, url }) => (
                <DocumentCard
                  key={id}
                  id={id}
                  createdAt={createdAt}
                  name={name}
                  url={url}
                  type={type}
                  onDelete={(id) => handleDelete(id)}
                />
              ))}
        </SimpleGrid>
      </Stack>
      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>New document</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {isCreatingDocument && (
              <Center>
                <Stack alignItems="center" spacing={6} marginY="100px">
                  <Spinner size="sm" />
                  <Text color="gray.500">Creating document...</Text>
                </Stack>
              </Center>
            )}
            {!isCreatingDocument && (
              <Stack spacing={4}>
                {shouldShowPsychic && (
                  <HStack
                    backgroundColor="gray.800"
                    borderRadius="md"
                    padding={4}
                    spacing={5}
                    justifyContent="space-between"
                  >
                    <HStack spacing={6}>
                      <NextImage
                        src="/psychic-logo.png"
                        alt="Psychic"
                        width="40"
                        height="40"
                      />
                      <Stack spacing={0}>
                        <HStack>
                          <Text as="b">Psychic</Text>{" "}
                          <Tag
                            colorScheme="green"
                            size="sm"
                            borderRadius="full"
                          >
                            New
                          </Tag>
                        </HStack>

                        <Text fontSize="sm" noOfLines={1} color="gray.500">
                          Connect to Google Drive, Jira, Zendesk, Dropox etc.
                        </Text>
                      </Stack>
                    </HStack>
                    <Button
                      isDisabled={!isReady}
                      onClick={onConnectAPI}
                      isLoading={isLoading}
                    >
                      Connect
                    </Button>
                  </HStack>
                )}
                <Stack>
                  <FormControl isRequired isInvalid={errors?.name}>
                    <FormLabel>Name</FormLabel>
                    <Input
                      type="text"
                      {...register("name", { required: true })}
                    />
                    <FormHelperText>A document name.</FormHelperText>
                    {errors?.name && (
                      <FormErrorMessage>Invalid name</FormErrorMessage>
                    )}
                  </FormControl>
                  {documentType === "URL" ? (
                    <FormControl isRequired isInvalid={errors?.url}>
                      <FormLabel>URL</FormLabel>
                      <Textarea
                        placeholder="Comma separated list of urls..."
                        {...register("url", { required: true })}
                      />
                      <FormHelperText>
                        A comma separated list of urls.
                      </FormHelperText>
                      {errors?.url && (
                        <FormErrorMessage>Invalid URL</FormErrorMessage>
                      )}
                    </FormControl>
                  ) : (
                    <FormControl isRequired isInvalid={errors?.url}>
                      <FormLabel>URL</FormLabel>
                      <Input
                        type="text"
                        {...register("url", { required: true })}
                      />
                      <FormHelperText>
                        A publicly accessible URL to your document.
                      </FormHelperText>
                      {errors?.url && (
                        <FormErrorMessage>Invalid URL</FormErrorMessage>
                      )}
                    </FormControl>
                  )}

                  <FormControl isRequired isInvalid={errors?.type}>
                    <FormLabel>Type</FormLabel>
                    <Select {...register("type", { required: true })}>
                      <option value="PDF">PDF</option>
                      <option value="CSV">CSV</option>
                      <option value="TXT">TXT</option>
                      <option value="URL">URL</option>
                      <option value="YOUTUBE">Youtube</option>
                      <option value="MARKDOWN">Markdown</option>
                    </Select>
                    {errors?.type && (
                      <FormErrorMessage>Invalid type</FormErrorMessage>
                    )}
                  </FormControl>
                  {documentType === "OPENAPI" && (
                    <FormControl>
                      <Alert variant="solid" colorScheme="red">
                        This feature is exeperimental, use with caution.
                      </Alert>
                      <Stack marginTop={4}>
                        <FormLabel>Authorization</FormLabel>
                        <HStack>
                          <Select {...register("auth_type")}>
                            <option value="header">Header</option>
                            <option value="query">Query params</option>
                          </Select>
                          <Input
                            placeholder="Header or query param key"
                            type="text"
                            {...register("auth_key")}
                          />
                        </HStack>
                        <Box>
                          <Input
                            placeholder="Header or query param value"
                            type="text"
                            {...register("auth_value")}
                          />
                          <FormHelperText>
                            If the OpenApi spec your are using requires
                            authentication you need to use the fields above.
                          </FormHelperText>
                        </Box>
                      </Stack>
                    </FormControl>
                  )}
                </Stack>
              </Stack>
            )}
          </ModalBody>
          <ModalFooter>
            <Button
              variant="ghost"
              mr={3}
              onClick={onClose}
              isDisabled={isCreatingDocument}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={isSubmitting || isCreatingDocument}
              isDisabled={isCreatingDocument}
            >
              Create
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Stack>
  );
}