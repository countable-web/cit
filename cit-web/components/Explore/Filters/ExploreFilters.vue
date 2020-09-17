<template>
  <div>
    <RegionalDistricts
      ref="regionalDistrictsFilter"
      class="d-inline-block mb-3"
      @filter="handleFilter"
    ></RegionalDistricts>
    <CommunityType
      ref="communityTypeFilter"
      class="d-inline-block mb-3"
      @filter="handleFilter"
    ></CommunityType>
    <Locations
      ref="locationsFilter"
      class="d-inline-block mb-3"
      @filter="handleFilter"
    ></Locations>
    <PopGrowth
      ref="popGrowthFilter"
      class="d-inline-block mb-3"
      @filter="handleFilter"
    ></PopGrowth>
    <Connectivity
      ref="connectivityFilter"
      class="d-inline-block mb-3"
      @filter="handleFilter"
    ></Connectivity>
    <MoreFilters class="d-inline-block"></MoreFilters>
  </div>
</template>

<script>
import { Component, Vue } from 'nuxt-property-decorator'
import isEmpty from 'lodash/isEmpty'
import CommunityType from '~/components/Explore/Filters/CommunityType'
import PopGrowth from '~/components/Explore/Filters/PopGrowth'
import RegionalDistricts from '~/components/Explore/Filters/RegionalDistricts'
import Connectivity from '~/components/Explore/Filters/Connectivity'
import MoreFilters from '~/components/Explore/Filters/MoreFilters'
import Locations from '~/components/Explore/Filters/Locations'
import { advancedSearch } from '~/api/cit-api'

@Component({
  CommunityType,
  MoreFilters,
  PopGrowth,
  Locations,
  RegionalDistricts,
  Connectivity,
})
export default class ExploreFilters extends Vue {
  handleFilter() {
    const refs = this.$refs
    let filterParams = {}
    for (const prop in refs) {
      const exploreFilter = refs[prop]
      exploreFilter.getParams().map((fp) => {
        filterParams = Object.assign(filterParams, fp)
      })
    }

    if (isEmpty(filterParams)) {
      this.$emit('filtered', { empty: true })
      return
    }

    advancedSearch(filterParams).then((result) => {
      this.$emit('filtered', { empty: false, data: result.data })
    })
  }
}
</script>