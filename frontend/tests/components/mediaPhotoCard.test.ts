import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, expect, it } from 'vitest'
import PhotoCard from '../../module_layers/media/frontend/components/media/PhotoCard.vue'

function doc(mime: string) {
  return {
    id: '00000000-0000-0000-0000-000000000001',
    title: 'IMG0001.dcm',
    mime_type: mime,
    thumb_url: null,
    full_url: '/api/v1/media/documents/1/download'
  }
}

describe('PhotoCard non-image placeholder (#565)', () => {
  it('never renders <img> for a DICOM document', async () => {
    const wrapper = await mountSuspended(PhotoCard, {
      props: { document: doc('application/dicom') }
    })
    expect(wrapper.find('img').exists()).toBe(false)
    expect(wrapper.find('div').exists()).toBe(true)
  })
})
