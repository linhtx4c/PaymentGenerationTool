<?php
declare(strict_types=1);

namespace VendorName\ModuleName\Gateway\Request;

use Magento\Payment\Gateway\Request\BuilderInterface;

class CommandNameRequestBuilderData implements BuilderInterface
{

    /**
     * @param array $buildSubject
     * @return array[]
     */
    public function build(array $buildSubject)
    {

        $paymentDO = SubjectReader::readPayment($handlingSubject);
        $payment = $paymentDO->getPayment();
        $ordere = $paymentDO->getOrder();

        return [
        ];
    }
}
