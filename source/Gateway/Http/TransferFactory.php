<?php
declare(strict_types=1);

namespace VendorName\ModuleName\Gateway\Http;

use Magento\Framework\Exception\NoSuchEntityException;
use VendorName\ModuleName\Gateway\Config\Config;
use Magento\Payment\Gateway\Http\Transfer;
use Magento\Payment\Gateway\Http\TransferBuilder;
use Magento\Payment\Gateway\Http\TransferFactoryInterface;
use Magento\Payment\Gateway\Http\TransferInterface;
use Magento\Framework\Webapi\Rest\Request;

/**
 * Class TransferFactory
 */
class TransferFactory implements TransferFactoryInterface
{

    /**
     * @var TransferBuilder
     */
    protected TransferBuilder $transferBuilder;

    /**
     * @var Config
     */
    protected Config $config;

    /**
     * InitializeFactory constructor.
     *
     * @param TransferBuilder $transferBuilder
     * @param Config $config
     */
    public function __construct(
        TransferBuilder       $transferBuilder,
        Config                $config
    )
    {
        $this->transferBuilder = $transferBuilder;
        $this->config = $config;
    }

    /**
     * @param array $request
     * @return Transfer|TransferInterface
     * @throws NoSuchEntityException
     */
    public function create(array $request)
    {
        $uri = '';
        return $this->transferBuilder
            ->setHeaders([
                "Content-Type" => "application/json"
            ])
            ->setBody($request)
            ->setUri($uri)
            ->build();
    }

}
