<?php
declare(strict_types=1);

namespace VendorName\ModuleName\Gateway\Http\Client;

use GuzzleHttp\Exception\GuzzleException;
use Magento\Framework\Serialize\SerializerInterface;
use Magento\Payment\Gateway\Http\ClientInterface;
use Magento\Payment\Gateway\Http\TransferInterface;
use GuzzleHttp\ClientFactory;
use Psr\Log\LoggerInterface;
use Throwable;

/**
 * Class Client
 */
class Client implements ClientInterface
{

    /**
     * @var ClientFactory
     */
    private ClientFactory $clientFactory;

    /**
     * @var SerializerInterface
     */
    private SerializerInterface $serializer;

    /**
     * @var LoggerInterface
     */
    private LoggerInterface $logger;

    /**
     * @param ClientFactory $clientFactory
     * @param SerializerInterface $serializer
     * @param LoggerInterface $logger
     */
    public function __construct(
        ClientFactory       $clientFactory,
        SerializerInterface $serializer,
        LoggerInterface     $logger
    )
    {
        $this->clientFactory = $clientFactory;
        $this->serializer = $serializer;
        $this->logger = $logger;
    }

    /**
     * @param TransferInterface $transfer
     * @return array|bool|float|int|string|null
     * @throws Throwable
     * @throws GuzzleException
     */
    public function placeRequest(TransferInterface $transfer)
    {

        try {
            $client = $this->clientFactory->create();
            $requestOption = [
                'headers' => $transfer->getHeaders()
            ];

            if (!empty($transfer->getBody())) {
                $requestOption['body'] = $this->serializer->serialize($transfer->getBody());
            }

            $response = $client->request($transfer->getMethod(), $transfer->getUri(), $requestOption)
                ->getBody()
                ->getContents();

            return $this->serializer->unserialize($response);
        } catch (GuzzleException $e) {
            $this->logger->critical($e->getMessage());
            throw new \Exception('Transaction has been declined. Please try again later.');
        } catch (Throwable $e) {
            $this->logger->critical($e->getMessage());
            throw $e;
        }
    }

}
