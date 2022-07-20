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

#include "fstapi.h"
#include "fstext.h"

#define TSLIST_START_SIZE	1024

static struct fstTsList *tsListAlloc()
{
	struct fstTsList *tslist = calloc(1, sizeof(struct fstTsList));
	if (tslist == NULL)
		return NULL;

	tslist->size = TSLIST_START_SIZE;
	tslist->val = malloc(TSLIST_START_SIZE * sizeof(uint64_t));
	if (tslist->val == NULL) {
		free(tslist);
		return NULL;
	}

	return tslist;
}

static inline struct fstTsList *tsListAdd(struct fstTsList *tslist, uint64_t val)
{
	// expand -> realloc
	if (tslist->nvals >= tslist->size) {
		//printf("debug: before realloc: val@0x%lX, size=%i\n", tslist->val, tslist->size);
		tslist->size *= 2;
		tslist->val = realloc(tslist->val, tslist->size * sizeof(uint64_t));
		if (tslist->val == NULL)
			return NULL;
		//printf("debug:  after realloc: val@0x%lX, size=%i\n", tslist->val, tslist->size);
	}

	// add
	tslist->val[tslist->nvals++] = val;

	return tslist;
}

static void tsListFree(struct fstTsList *tslist)
{
	free(tslist->val);
	free(tslist);
}


static void tsValueChangeCallback(void *user_callback_data_pointer, uint64_t time, fstHandle facidx, const unsigned char *value)
{
	struct fstTsList **tslist_ptr = (struct fstTsList**)user_callback_data_pointer;
	struct fstTsList *tslist = *tslist_ptr;

	if (tslist == NULL)
		return;

	// ignore if timestamp is less or equal last
	if ((tslist->nvals > 0) && (time <= tslist->val[tslist->nvals-1]))
		return;

	*tslist_ptr = tsListAdd(tslist, time);
}

struct fstTsList *fstReaderGetTimestamps(void *ctx)
{
	struct fstTsList *tslist = tsListAlloc();
	if (tslist == NULL)
		return NULL;

	int ret = fstReaderIterBlocks(ctx, tsValueChangeCallback, &tslist, NULL);
	if (!ret)
		return NULL;

	return tslist;
}

void fstReaderFreeTimestamps(struct fstTsList *tslist)
{
	tsListFree(tslist);
}
