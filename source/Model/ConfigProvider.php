<?php
declare(strict_types=1);

namespace VendorName\ModuleName\Model;

use VendorName\ModuleName\Gateway\Config\Config;

class ConfigProvider implements \Magento\Checkout\Model\ConfigProviderInterface
{

    /**
     * @var Config
     */
    protected Config $config;

    /**
     * @param Config $config
     */
    public function __construct(
        Config $config
    )
    {
        $this->config = $config;
    }

    /**
     * @return array
     */
    public function getConfig()
    {   

        if($this->config->isActive()) {
            return [];
        }

        return [
            'payment' => [
                Config::CODE => [
                    'title' => $this->config->getTitle()
                ]
            ]
        ];
    }
}
