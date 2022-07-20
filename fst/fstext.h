/*
 * fstlib extensions
 *
 * Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef FST_EXT_H
#define FST_EXT_H

#ifdef __cplusplus
extern "C" {
#endif


struct fstTsList {
	unsigned long size;	// allocated space (#elements)
	unsigned long nvals;	// #elements in list
	uint64_t *val;		// values
};

/*
 * Get a fstTsList containing all timestamps of signals
 * selected by FacProcessMask
 * returns NULL on error
 */
struct fstTsList *fstReaderGetTimestamps(void *ctx);

/*
 * Free the fstTsList allocated by fstReaderGetTimestamps
 */
void fstReaderFreeTimestamps(struct fstTsList *tslist);


#ifdef __cplusplus
}
#endif

#endif
