import { useEffect, useState } from "react";
import { validatePhone } from "@/lib/phoneUtils";

export function usePhoneValidation(phoneValue: string, countryCode?: string) {
  const [isValid, setIsValid] = useState<boolean>(false);

  useEffect(() => {
    const validation = validatePhone(phoneValue, countryCode);
    setIsValid(validation.isValid);
  }, [phoneValue, countryCode]);

  return { isValid };
}
