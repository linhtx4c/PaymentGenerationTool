<?php

declare(strict_types=1);

namespace VendorName\ModuleName\Gateway\Config;

class Config extends \Magento\Payment\Gateway\Config\Config
{

    const CODE = 'payment_code';
    const ACTIVE = 'active';
    const TITLE = 'title';

    /**
     * @param ScopeConfigInterface $scopeConfig
     * @param string|null $methodCode
     */
    public function __construct(ScopeConfigInterface $scopeConfig, $methodCode = self::CODE)
    {
        parent::__construct($scopeConfig, $methodCode);
    }

    /**
     * @param $storeId
     * @return mixed|null
     */
    public function isActive($storeId = null)
    {
        return $this->getValue(self::ACTIVE, $storeId);
    }

    /**
     * @param $storeId
     * @return mixed|null
     */
    public function getTitle($storeId = null)
    {
        return $this->getValue(self::TITLE, $storeId);
    }
}