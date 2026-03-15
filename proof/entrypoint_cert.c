#include <string.h>
#include <x509/x509-cert-parser.h>

#if defined(__FRAMAC__)
#include "__fc_builtin.h"
#endif

int main(void)
{
	cert_parsing_ctx cert_ctx;
	volatile u8 input_buf[ASN1_MAX_BUFFER_SIZE];
	volatile u32 input_len = 0;

	memset(&cert_ctx, 0, sizeof(cert_ctx));

#if defined(__FRAMAC__)
	Frama_C_make_unknown((void *)input_buf, sizeof(input_buf));
	input_len = Frama_C_unsigned_int_interval(0, ASN1_MAX_BUFFER_SIZE);
#endif

	return parse_x509_cert(&cert_ctx,
			       (const u8 *)(const void *)input_buf,
			       (u32)input_len);
}
